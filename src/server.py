import socket
import threading
import time
from src.response import generate_page, generate_message_user_disconnection
from src.handler import send_message_to_clients, keep_alive, assign_user

HOST = '10.0.10.24'  # Change this to your local IP address
PORT = 8080  # Change this to your desired port

MESSAGES = []
CONNECTED_CLIENTS = []
USED_USERS = []
LAST_TIME_DISCONNECT = 0
LAST_TIME_CONNECT = 0
KEEP_USER = -1

def handle_client(conn, addr):
    """
    Handles communication with a single client.

    Args:
        conn (socket.socket): The client connection socket.
        addr (tuple): The address of the client.
    """
    global KEEP_USER, LAST_TIME_CONNECT, LAST_TIME_DISCONNECT
    LAST_TIME_CONNECT = time.time()
    print('Connected by', addr)
    CONNECTED_CLIENTS.append(conn)
    print(f"Connected clients: {len(CONNECTED_CLIENTS)}")
    try:
        response = generate_page(messages=MESSAGES)
        conn.sendall(response.encode('utf-8'))
        time.sleep(0.01)
        user, KEEP_USER = assign_user(addr, LAST_TIME_DISCONNECT, USED_USERS, MESSAGES, KEEP_USER, CONNECTED_CLIENTS)
        keep_alive(conn, user, MESSAGES, CONNECTED_CLIENTS)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        CONNECTED_CLIENTS.remove(conn)
        LAST_TIME_DISCONNECT = time.time()
        KEEP_USER = user
        if time.time() - LAST_TIME_CONNECT > 0.1:
            client_disconnection_message = generate_message_user_disconnection(addr[0],user)
            MESSAGES.append((user, client_disconnection_message))
            send_message_to_clients(client_disconnection_message, CONNECTED_CLIENTS)
            print('Disconnected by', addr)
            print(f"Connected clients: {len(CONNECTED_CLIENTS)}")

def start_server():
    """
    Starts the server and listens for incoming connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started at http://{HOST}:{PORT}")
        while True:
            try:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
            except KeyboardInterrupt:
                print("\nClosing server")
                break
        s.close()