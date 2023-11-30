#!/usr/bin/env python3
"""Functions to transform/visualize GoT data."""
import warnings
from os.path import join
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.signal import medfilt
from scipy.spatial.distance import cdist

from ebl_coords.backend.constants import SCALE, TOLERANCE


def mark_valid_signal(
    df: pd.DataFrame,
    min_level: np.uint8 = 10,
    min_distance: np.uint32 = 6_000,
    max_distance: np.uint32 = 12_000,
) -> Tuple[pd.DataFrame, np.ndarray]:
    """Flag all Points that are valid, applying GoT constraints.

       constraints from GOT-HelpGuide-EN.pdf page 23
       constraints from GT_Command_manual.pdf page 111

    Args:
        df (pd.DataFrame): Dataframe containing raw GoT tcp output.
        min_level (np.uint8, optional): minimal signal strength from 0 - 255. Defaults to 10.
        min_distance (np.uint32, optional): minimal distance from transmitter to receiver from 1 - 6_000. Defaults to 6_000.
        max_distance (np.uint32, optional): maximal distance from transmitter to receiver from 12_000 - 15_000. Defaults to 12_000.

    Returns:
        pd.DataFrame: flagged Dataframe
        np.ndarray: array with shape (points, receivers)
    """
    number_recv = int((df.shape[1] - 6) / 3)
    recv_flg = np.zeros((df.shape[0], number_recv), dtype=int)
    recv_df = df.iloc[:, 7:]
    for i in range(number_recv):
        temp = recv_df.iloc[:, i * 3 + 1 : i * 3 + 3]
        distance = temp.iloc[:, 0]
        level = temp.iloc[:, 1]

        recv_flg[:, i] = (
            (distance >= min_distance)
            & (distance < max_distance)
            & (level >= min_level)
        )
    df.insert(0, "got_signal_flg", recv_flg.sum(axis=1) >= 3)
    return df, recv_flg


def get_df(
    files: List[str], folder: Optional[str] = None, keep_unique: bool = True
) -> pd.DataFrame:
    """Transform raw GoT Output files into one Dataframe.

    Args:
        files (List[str]): List of filenames
        folder (Optional[str], optional): Folder containing all the files. Example: './data/'.
                                          (None equals to the current folder).
        keep_unique (bool): If True keep all columns with only one same value.

    Returns:
        pd.DataFrame: Dataframe with named columns if known.
    """
    frames = []
    for file in files:
        if folder is not None:
            file = join(folder, file)
        temp = pd.read_csv(file, sep="[,|;]", engine="python", header=None)
        frames.append(temp)

    df = pd.concat(frames, ignore_index=True, axis=0)
    df.drop(df.columns[-1], axis=1, inplace=True)
    df.rename(columns={df.columns[0]: "pc_timestamp"}, inplace=True)
    df.rename(columns={df.columns[1]: "time_after_start_ms"}, inplace=True)
    df.rename(columns={df.columns[2]: "transmitter_id"}, inplace=True)
    df.rename(columns={df.columns[3]: "valid_flg"}, inplace=True)
    df.rename(columns={df.columns[4]: "x"}, inplace=True)
    df.rename(columns={df.columns[5]: "y"}, inplace=True)
    df.rename(columns={df.columns[6]: "z"}, inplace=True)
    for i in range(7, df.shape[1] - 1, 3):
        k = int((i - 6) / 3)
        df.rename(columns={df.columns[i]: f"receiver_id_{k}"}, inplace=True)
        df.rename(columns={df.columns[i + 1]: f"distance_{k}"}, inplace=True)
        df.rename(columns={df.columns[i + 2]: f"level_{k}"}, inplace=True)

    if not keep_unique:
        for col in df.columns:
            if np.unique(df[[col]]).shape[0] == 1:
                df.drop(columns=[col], inplace=True)

    return df


def to_img_arr(
    df: pd.DataFrame, scale: float = SCALE, value: np.uint8 = 255
) -> Tuple[np.ndarray, pd.DataFrame]:
    """Build an 2d Array representing a png of measured points and create lookup columns in the Dataframe.

    Args:
        df (pd.DataFrame): Dataframe with u, v (image coords) and morph_flg = False.
        scale (float, optional): Scalingfactor of the image. Defaults to SCALE.
        value (np.uint8, optional): Fillvalue of coordinates. Defaults to 255.

    Returns:
        Tuple[np.ndarray, pd.DataFrame]: Array representing a greyscale picture. Transformed Dataframe.
    """
    x = df.x.to_numpy(dtype=np.int32)
    y = df.y.to_numpy(dtype=np.int32)
    x += np.abs(x.min())
    y += np.abs(y.min())

    w = x.max()
    h = y.max()
    w = int(w * scale)
    h = int(h * scale)

    arr = np.zeros((h + 1, w + 1), dtype=np.uint8)

    u = (y * scale).astype(np.int32)
    v = (x * scale).astype(np.int32)

    arr[(u, v)] = value

    df.insert(0, "u", u)
    df.insert(1, "v", v)

    return arr, df


def mark_tolerance(
    df: pd.DataFrame,
    tolerance: int = TOLERANCE,
    lower_bnd: Optional[int] = None,
    upper_bnd: Optional[int] = None,
) -> pd.DataFrame:
    """Mark good points.

        If:
            - it is the firt or last point
            - z coordinate is outside of given boundary
            - the distance to the closest neighbour is <= tolerance

    Args:
        df (pd.DataFrame): DataFrame with GoT-Coords in x, y, z columns.
        tolerance (int, optional): Minimal distance to closest neighbour. Defaults to TOLERANCE.
        lower_bnd (int, optional): Lower boundary for z. Defaults to None.
        upper_bnd (int, optional): Upper boundary for z. Defaults to None.

    Returns:
        pd.DataFrame: Dataframe with marked_tolerance_lowerbnd_upperbnd column.
    """
    # z boundary
    marked = df.z.to_numpy()
    if lower_bnd:
        lower_marked = marked >= lower_bnd
    else:
        lower_marked = np.full(marked.shape, True)
    if upper_bnd:
        upper_marked = marked <= upper_bnd
    else:
        upper_marked = np.full(marked.shape, True)
    marked = lower_marked & upper_marked

    coords = np.c_[df.x, df.y, df.z]
    # scatter & and reduce with minus
    d = coords[1:, :] - coords[:-1, :]
    # calculate norm
    d = np.apply_along_axis(np.linalg.norm, axis=1, arr=d)

    # scatter
    d_mask = np.c_[d[:-1], d[1:]]
    # reduce with min
    d_mask = d_mask.min(axis=1) <= tolerance

    # ignore first and last point, because it only has one neighbour
    marked[0] = False
    marked[-1] = False
    # combine bothe constraints
    marked[1:-1] = marked[1:-1] & d_mask

    df.insert(0, f"marked_{tolerance}_{lower_bnd}_{upper_bnd}", marked)

    return df


def keep_k_coeff(
    a: np.ndarray, n: int = 1, percent: Optional[float] = None
) -> np.ndarray:
    """Keep only the first n fft coefficients sorted by magnitude.

    Args:
        a (np.ndarray): fft coefficients array
        n (int, optional): How many coefficients to keep. Defaults to 1.
        percent (float, optional): How many coefficients to keep as percent [0, 1], will override n. Default is None.

    Returns:
        np.ndarray: _description_
    """
    if percent is not None:
        n = int(a.size * percent)
        print(f"used {n} / {a.size}")
    magnitudes = np.abs(a)
    idx = np.argpartition(magnitudes, -n, axis=None)[:-n]
    idx = np.unravel_index(idx, a.shape)
    a[idx] = 0
    return a


def median_filter(
    coords: np.ndarray,
    kernel_size: np.uint,
) -> np.ndarray:
    """Use median filter on given coordinates.

    Each Axis is treated individually.
    If part of the kernel is outside, ignore values and drop them.

    Args:
        coords (np.ndarray): Input coordinates
        kernel_size (np.uint): length of the 1d kernel

    Returns:
        np.ndarray: modified coordinates
    """
    hotspot = int(kernel_size / 2)
    return np.apply_along_axis(
        lambda col: medfilt(col, kernel_size), arr=coords, axis=0
    )[hotspot:-hotspot]


def get_track_switches_hit(
    labels: np.ndarray,
    label_coords: np.ndarray,
    waypoints: np.ndarray,
    threshold: float,
) -> np.ndarray:
    """Get all labels, which near any waypoint.

    Raise Warning if not all waypoint are distinctively mapped.

    Args:
        labels (np.ndarray): lables of coords labels-length = number of label_coords
        label_coords (np.ndarray): coordinates of labels
        waypoints (np.ndarray): any waypoints
        threshold (float): radius <= of sphere around label_coords

    Returns:
        np.ndarray: All labels which have at least one waypoint in threshold distance.
    """
    distances = cdist(label_coords, waypoints)
    distances = distances <= threshold
    labels_hits = distances.sum(axis=1)
    warnings.warn(f"double hits: {distances.sum(axis=0).max() > 1}")
    return labels[labels_hits > 1]


def filter_df(
    df: pd.DataFrame,
    kernel_size: Optional[int] = 11,
    tolerance: Optional[int] = TOLERANCE,
) -> pd.DataFrame:
    """Filter all outliers in df.

    Args:
        df (pd.DataFrame): df
        kernel_size (Optional[int], optional): kernel size of median filter, set to None for no median filter. Defaults to 11.
        tolerance (Optional[int], optional): Minimal distance to closest neighbour needed to be valid, None = infinite. Defaults to TOLERANCE.

    Returns:
        pd.DataFrame: transformed df
    """
    if tolerance:
        df = mark_tolerance(df, tolerance=tolerance, lower_bnd=None, upper_bnd=None)
        df = df.loc[df.iloc[:, 0]]

    if kernel_size:
        median_coords = median_filter(np.c_[df.x, df.y, df.z], kernel_size)
        k = kernel_size // 2
        df = df.iloc[k:-k, :]
        df.loc[:, ["x", "y", "z"]] = median_coords
    return df
