import json
import socket
import threading
from typing import List
from ebl_coords.backend.command.command import Command
from ebl_coords.backend.observable.gtcommand_subject import GtCommandSubject
from ebl_coords.backend.observable.observer import Observer
from ebl_coords.decorators import override
from ebl_coords.backend.constants import POSITION_INTERFACE_PORT


class InterfacePositionObserver(Observer):
    def __init__(self) -> None:
        print("Initializing interface position observer")

        self.clients: List[socket.socket] = []
        self.server_socket = None

        self.start_server()


    def start_server(self):
        """Start the TCP socket server to accept connections from clients."""

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", POSITION_INTERFACE_PORT))  # Bind to all interfaces on port 9000
        self.server_socket.listen(5)  # Listen for up to 5 clients

        print("Position interface started, waiting for clients to connect...")

        # Start a thread to handle client connections
        threading.Thread(target=self.accept_clients, daemon=True).start()


    def accept_clients(self):
        """Accept incoming client connections."""

        while True:
            client_socket, client_address = self.server_socket.accept()

            print(f"Position Interface: Client connected from {client_address}")

            self.clients.append(client_socket)

            # Start a thread to handle the client
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()


    def handle_client(self, client_socket: socket.socket):
        """Handle a single client connection."""

        try:
            while True:
                # This is a placeholder for reading client data if needed
                # data = client_socket.recv(1024).decode('utf-8')
                pass
        except (ConnectionResetError, BrokenPipeError):
            print("Position Interface: Client disconnected", client_socket)
        finally:
            client_socket.close()
            self.clients.remove(client_socket)

    @override
    def update(self) -> None:
        transmitter_id, timestamp, coord = self.result
        coord_list = coord.tolist()

        self.broadcast(json.dumps({
            "transmitterId": transmitter_id,
            "timestamp": timestamp,
            "coordinate": coord_list
        }))

    
    def broadcast(self, coord: str):
        coord = coord + ";"
        for client_socket in self.clients:
            try:
                client_socket.sendall(coord.encode('utf-8'))
            except (ConnectionResetError, BrokenPipeError):
                print("Position interface: Connnection lost to client", client_socket)
                client_socket.close()
                self.clients.remove(client_socket)


class AttachPushPositionToInterfaceCommand(Command):
    def __init__(self) -> None:
        super().__init__(None, GtCommandSubject())

        self.context: GtCommandSubject

    @override
    def run(self) -> None:
        self.context.attach_changed_coord(InterfacePositionObserver())