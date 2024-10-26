"""Provide a simple socket connection to GtCommand."""
from __future__ import annotations

import socket
from threading import RLock, Thread
from typing import TYPE_CHECKING

import numpy as np

from ebl_coords.backend.constants import GTCOMMAND_IP, GTCOMMAND_PORT, IGNORE_Z_AXIS
from ebl_coords.backend.constants import TS_HIT_THRESHOLD
from ebl_coords.backend.observable.subject import Subject
from ebl_coords.backend.transform_data import get_tolerance_mask, get_track_switches_hit
from ebl_coords.decorators import override
from ebl_coords.graph_db.data_elements.switch_item_enum import SwitchItem
from ebl_coords.graph_db.graph_db_api import GraphDbApi

if TYPE_CHECKING:
    from ebl_coords.backend.observable.observer import Observer


class GtCommandSubject(Subject):
    """GtCommand Subject."""

    def __init__(
        self,
        median_kernel_size: int = 11,
        noise_filter_threshold: int = 30,
        ip: str = GTCOMMAND_IP,
        port: int = GTCOMMAND_PORT,
        ts_hit_threshold: int = TS_HIT_THRESHOLD,
    ) -> None:
        """Initialize the buffer and the socket.

        Args:
            median_kernel_size (int, optional): kernel size used for median filter. Defaults to 11.
            noise_filter_threshold (int, optional): Maximal allowed distance between neighbouring points. Defaults to 30.
            ip (str, optional): ip of GtCommand. Defaults to GTCOMMAND_IP.
            port (int, optional): port of GtCommand. Defaults to GTCOMMAND_PORT.
            ts_hit_threshold(int, optional): Maximal distance coord to trainswitch to be considered valid hit. Defaults to 35.
        """
        super().__init__()
        self.graph_db = GraphDbApi()
        self.ts_coords: np.ndarray
        self.ts_labels: np.ndarray | None = None
        self.ip: str = ip
        self.port: int = port
        self.ts_hit_threshold = ts_hit_threshold
        self.loc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.record_thread = Thread(
            target=self._record,
            daemon=True,
            args=[noise_filter_threshold],
        )
        self.record_thread.start()

        self.all_coord_observers: list[Observer] = []
        self.changed_coord_observers: list[Observer] = []
        self.ts_hit_observers: list[Observer] = []

        self._median_kernel_size = median_kernel_size
        self._noise_buffer = dict()
        self._median_buffer = dict()
        self.ts_coords_lock = RLock()
        self.ts_labels_lock = RLock()

    def get_noise_buffer(self, transmitter_id: str) -> np.ndarray:
        if not transmitter_id in self._noise_buffer:
            self._noise_buffer[transmitter_id] = np.full((3, 3), dtype=np.float32, fill_value=np.nan)

        return self._noise_buffer.get(transmitter_id)
    
    def set_noise_buffer(self, transmitter_id: str, noise_buffer: np.ndarray) -> None:
        self._noise_buffer[transmitter_id] = noise_buffer

    def get_median_buffer(self, transmitter_id: str) -> np.ndarray:
        if not transmitter_id in self._median_buffer:
            self._median_buffer[transmitter_id] = np.full((self._median_kernel_size, 3), dtype=np.float32, fill_value=np.nan)

        return self._median_buffer.get(transmitter_id)
    
    def set_median_buffer(self, transmitter_id: str, median_buffer: np.ndarray) -> None:
        self._median_buffer[transmitter_id] = median_buffer

    def set_next_ts(self, edge_id: str) -> None:
        """Set coordinates and label of following node after this edge.

        Args:
            edge_id (str): edge_id
        """
        weiche = SwitchItem.WEICHE.name
        cmd = f"""
        MATCH ({weiche})-[r]->(n:{weiche})\
        WHERE r.edge_id='{edge_id}'\
        RETURN n.node_id, n.x, n.y, n.z
        """
        df = self.graph_db.run_query(cmd)
        with self.ts_coords_lock:
            self.ts_coords = df[["n.x", "n.y", "n.z"]].to_numpy().astype(np.float32)
            if IGNORE_Z_AXIS:
                self.ts_coords[:, 2] = 0
        with self.ts_labels_lock:
            self.ts_labels = df["n.node_id"].to_numpy()

    def _filter_coord(self, transmitter_id: str, coord: np.ndarray, noise_filter_threshold: int) -> np.ndarray | None:
        med_coord: np.ndarray | None = None
        _noise_buffer = self.get_noise_buffer(transmitter_id)
        _noise_buffer[-1] = coord
        if get_tolerance_mask(_noise_buffer, noise_filter_threshold)[0]:
            _median_buffer = self.get_median_buffer(transmitter_id)
            _median_buffer[-1] = _noise_buffer[1]
            if not np.isnan(_median_buffer).any():
                med_coord = np.median(_median_buffer, axis=0)
            _median_buffer = np.roll(_median_buffer, shift=_median_buffer.size - 3)
            self.set_median_buffer(transmitter_id, _median_buffer)

        _noise_buffer = np.roll(_noise_buffer, shift=_noise_buffer.size - 3)
        self.set_noise_buffer(transmitter_id, _noise_buffer)
        return med_coord

    def _record(self, noise_filter_threshold: int) -> None:
        buffer = b""
        self.loc_socket.connect((self.ip, self.port))
        last_coord: np.ndarray | None = None
        ts_last_hit: np.ndarray | None = None
        while True:
            while b";" not in buffer:
                buffer += self.loc_socket.recv(1024)

            line, _, buffer = buffer.partition(b";")
            line_string = line.decode("utf-8")

            ds = line_string.split(",")
            coord = np.array([ds[3], ds[4], ds[5]], dtype=np.int32)
            time_stamp = int(ds[0])
            transmitter_id = int(ds[1])
            filtered_coord = self._filter_coord(transmitter_id, coord, noise_filter_threshold)
            if filtered_coord is not None:
                self.notify(self.all_coord_observers, filtered_coord)
                if not np.all(filtered_coord == last_coord):
                    if IGNORE_Z_AXIS:
                        filtered_coord[2] = 0
                    self.notify(self.changed_coord_observers, (transmitter_id, time_stamp, filtered_coord))
                    if self.ts_labels and self.ts_hit_observers:
                        with self.ts_labels_lock:
                            with self.ts_coords_lock:
                                hit_labels = get_track_switches_hit(
                                    self.ts_labels,
                                    self.ts_coords,
                                    filtered_coord.reshape(1, -1),
                                    self.ts_hit_threshold,
                                )
                            last_coord = filtered_coord
                            if not np.all(ts_last_hit == hit_labels) and hit_labels.size > 0:
                                self.notify(self.ts_hit_observers, hit_labels)
                                ts_last_hit = hit_labels

    @override
    def attach(self, observer: Observer) -> None:
        """Attach observer.

        Args:
            observer (Observer): observer
        """
        with self.lock:
            self.changed_coord_observers.append(observer)

    def attach_all_coord(self, observer: Observer) -> None:
        """Attach observer that is notified whenever a new valid coordinate is received.

        observer.result contains the new coordinate as np.ndarray

        Args:
            observer (Observer): observer
        """
        observer.subject = self
        with self.lock:
            self.all_coord_observers.append(observer)

    def attach_changed_coord(self, observer: Observer) -> None:
        """Attach observer that is notified whenever a different coordinate is received.

        observer.result contains Tuple[int, np.ndarray] timestamp in ms, coordinate

        Args:
            observer (Observer): observer
        """
        observer.subject = self
        with self.lock:
            self.changed_coord_observers.append(observer)

    def attach_ts_hit(self, observer: Observer) -> None:
        """Attach observer that is notified whenever a train switch is hit.

        observer.result contains hit labels as np.ndarray

        Args:
            observer (Observer): observer
        """
        observer.subject = self
        with self.lock:
            self.ts_hit_observers.append(observer)

    def detach_all_coord(self, observer: Observer) -> None:
        """Detach observer from this hook.

        Args:
            observer (Observer): observer
        """
        with self.lock:
            self.all_coord_observers.remove(observer)

    def detach_changed_coord(self, observer: Observer) -> None:
        """Detach observer from this hook.

        Args:
            observer (Observer): observer
        """
        with self.lock:
            self.changed_coord_observers.remove(observer)

    def detach_ts_hit(self, observer: Observer) -> None:
        """Detach observer from this hook.

        Args:
            observer (Observer): observer
        """
        with self.lock:
            self.ts_hit_observers.remove(observer)

    @override
    def detach(self, observer: Observer) -> None:
        """Detach observer from all hooks.

        Args:
            observer (Observer): observer
        """
        with self.lock:
            if observer in self.all_coord_observers:
                self.all_coord_observers.remove(observer)
            if observer in self.changed_coord_observers:
                self.changed_coord_observers.remove(observer)
            if observer in self.ts_hit_observers:
                self.ts_hit_observers.remove(observer)
