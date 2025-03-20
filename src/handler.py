import time
from src.response import generate_message, generate_message_user_connection

def send_message_to_clients(message, connected_clients):
    """
    Sends a message to all connected clients.

    Args:
        message (str): The message to send.
    """
    for client in connected_clients:
        try:
            client.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to client: {e}")

def keep_alive(conn, user, messages, connected_clients):
    """
    Keeps the connection alive and listens for incoming messages.
    
    Args:
        conn (socket.socket): The client connection socket.
        user (int): The user number.
    """
    while True:
        resp = conn.recv(1024)
        if not resp:
            break
        resp = resp.decode('utf-8')
        message = " ".join(resp.split('\r\n')[-1].split('=')[-1].split('+'))
        if message:
            messages.append((user, message))
            message = generate_message(user, message)
            send_message_to_clients(message, connected_clients)

def assign_user(addr, last_time_disconnect, used_users, messages, keep_user, connected_clients):
    """
    Assigns a user number to a new client.
    
    Args:
        addr (str): The address of the client.
    
    Returns:
        int: The user number.
    """
    if time.time() - last_time_disconnect < 0.1 and keep_user != -1:
        user = keep_user
        keep_user = -1
    else:
        user = 1
        while user in used_users:
            user += 1
        used_users.append(user)
        client_connection_message = generate_message_user_connection(addr[0],user)
        messages.append((user, client_connection_message))
        send_message_to_clients(client_connection_message, connected_clients)
    return user, keep_user