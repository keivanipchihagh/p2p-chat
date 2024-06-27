import re
import socket
import requests
from typing import List

# Third-party imports
from config import (
    # API
    API_HOST,
    API_PORT
)



def show_menu():
    # Program CLI
    text = """
P2P Chat CLI
- /peers: Shows all available peers
- /connect {username:str}: Connects to a peer
- /help: Shows the menu
    """
    print(text)



def command_peers():
    """
        - /peers: Shows all available peers
    """
    response = requests.get(f"http://{API_HOST}:{API_PORT}/api/v1/peers")
    if response.status_code == 200:
        peers = response.json()
        for peer in peers:
            print(f"- {peer}")



def command_connect():
    """
        - /connect {username:str}: Connects to a peer
    """
    username = _input.split(" ")[1]
    response = requests.get(f"http://{API_HOST}:{API_PORT}/api/v1/peerinfo?username={username}")
    if response.status_code == 200:
        _: dict = response.json()
        host = _.get('host')
        port = _.get('port')
        connect(host, port)
    elif response.status_code == 404:
        print(f"Peer '{username}' not found.")
    else:
        print("Whoops! Something is on fire..")



def connect(host: str, port: int):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the socket to the specified host and port
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Send data
        message = "Hello, Server!"
        sock.sendall(message.encode('utf-8'))

        # Receive data
        data = sock.recv(1024)
        print(f"Received: {data.decode('utf-8')}")

    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the socket
        sock.close()
        print("Connection closed")



if __name__ == '__main__':
    while True:
        _input              = input("\nCommand: ")
        matches: List[str]  = re.findall(r'^/(\w+)', _input)

        if len(matches) == 0:
            show_menu()
        else:
            command = matches[0]
            if command == "peers":
                command_peers()
            elif command == "connect":
                command_connect()
            elif command == "help":
                show_menu()
