import socket
import requests
import threading
import json
from typing import List, Tuple

# Third-party imports
from utils import logger
from config import (
    # Peer
    PEER_HOST,
    PEER_PORT,
    PEER_USERNAME,
    # API
    API_HOST,
    API_PORT
)


def handle_incoming_connections(server_socket: socket.socket) -> None:
    """
        Handle incoming connections from clients. This function listens on a server socket
        and accepts incoming connections. For each connection, it creates a new thread to handle the client.

        Parameters:
            - server_socket (socket.socket): The server socket to listen on.
        Returns:
            - None
    """

    while True:
        connection: socket.socket
        connection, client_address = server_socket.accept() # Waits for an incoming connection (blocking)

        host: str = client_address[0]
        port: int = client_address[1]

        print()
        logger.debug(f"Connected to '{host}:{port}'...")
        read(connection)

        while True:
            message = input(f"(reply) >> ")
            write(connection, PEER_USERNAME, message)



def read(
    connection: socket.socket,
    threaded: bool = True
) -> None:
    """
        Reads incoming datat from a client from a thread. It reads data in chunks of 1024 bytes and decodes
        it from UTF-8. The function continues reading data from the client until it receives no more data.

        Parameters:
            - connection (socket.socket): The socket connection to the client.
            - threaded (bool): Whether to run the function on an other thread.

        Returns:
            - None
    """
    def _read():
        try:
            while True:
                data = connection.recv(1024)    # Read 1 KB
                if data:
                    payload: dict = json.loads(data.decode('utf-8'))

                    username: str   = payload.get('username')
                    message: str    = payload.get('message')

                    print()
                    logger.info(f"{username}: {message}")
                else:
                    break
        except socket.error as e:
            logger.error(f"Failed to read message")
        finally:
            connection.close()

    threading.Thread(target=_read).start()


def write(
    connection: socket.socket,
    username: str,
    message: str
) -> None:
    """
        Writes data to a client. It serializes the data into JSON and sends it over the socket connection.

        Parameters:
            - connection (socket.socket): The socket connection to the client.
            - username (str): The username of the sender.
            - message (str): The message to be sent.

        Returns:
            - None
    """
    try:
        payload = {
            "username": username,
            "message": message
        }
        data = json.dumps(payload).encode('utf-8')  # Serialize
        connection.sendall(data)
    except:
        logger.error(f"Failed to transmit message.")


def connect(
    host: str,
    port: int,
    username: str
) -> socket.socket:
    """
        Connects to a peer specified by its host and port and sends an initial handshake message.

        Parameters:
            - host (str): The host of the peer to connect to.
            - port (int): The port of the peer to connect to.
            - username (str): The username of the peer to connect to.

        Returns:
            - (socket.socket): Peer socket
    """
    # Connect to peer
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    logger.success(f"Connected to {username} ({host}:{port}).")

    # Write inital message
    write(connection, PEER_USERNAME, "Hello There!")

    # Start reading from peer
    read(connection)

    return connection



def get_peers() -> List[str]:
    """ Retrieves all available peers from the stun server """
    response = requests.get(f"http://{API_HOST}:{API_PORT}/api/v1/peers")
    if response.status_code == 200:
        peers: List[str] = response.json()
        return peers
    else:
        logger.error(f"Failed to retrieve peers (code: {response.status_code}).")



def register() -> None:
    """ Registers the peer in the stun server """
    response = requests.post(
        f"http://{API_HOST}:{API_PORT}/api/v1/register",
        json = {
            "username": PEER_USERNAME,
            "host": PEER_HOST,
            "port": PEER_PORT
        }
    )
    if response.status_code == 201:
        logger.success(f"Registered on the stun server.")
    elif response.status_code == 409:
        logger.warning(f"Username is taken. Use another one.")
    else:
        logger.error(f"Failed to register on the stun server (code: {response.status_code}).")



def get_peerinfo(username: str) -> Tuple[str, int]:
    response = requests.get(f"http://{API_HOST}:{API_PORT}/api/v1/peerinfo?username={username}")
    if response.status_code == 200:
        _: dict = response.json()
        host = _.get('host')
        port = int(_.get('port'))
        return host, port
    else:
        logger.error(f"Failed to retrieve peerinfo for '{username}' (code: {response.status_code}).")



def start_peer(
    ) -> None:

    # Listen to incoming connections and listen to each on a seperate thread.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((PEER_HOST, PEER_PORT))
    server_socket.listen(1)
    threading.Thread(target=handle_incoming_connections, args=(server_socket,)).start()
    logger.debug(f"Started listening on {PEER_HOST}:{PEER_PORT}...")


    while True:
        _: str = input(">> ")

        if _.startswith("/register"):
            register()
        elif _.startswith("/peers"):
            peers: List[str] = get_peers()
            logger.success(peers)

        elif _.startswith("/connect"):
            username = _.split(" ")[1]
            peers: List[str] = get_peers()

            if username not in peers:
                logger.warning(f"Peer '{username}' not among available peers. Aborted.")
                continue

            host, port = get_peerinfo(username)
            logger.debug(f"Connecting to {username} ({host}:{port})...")

            try:
                connection = connect(host, port, username)

                while True:
                    message = input(f"[{username}] >> ")
                    write(connection, username, message)
            except:
                logger.error(f"Failed to connect to {username} ({host}:{port}).")

        else:
            pass



if __name__ == "__main__":
    logger.info(f"Your username: '{PEER_USERNAME}'")
    register()
    start_peer()
