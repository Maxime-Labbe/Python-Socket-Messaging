import socket
import threading

HOST = '192.168.1.87'  # Change this to your local IP address
PORT = 8080  # Change this to your desired port

MESSAGES = []
CONNECTED_CLIENTS = []

def generate_page():
    """
    Generates the HTML page with the current messages.

    Returns:
        str: The HTML page as a string.
    """
    messages_html = "".join(f"<p>{address} : {msg}</p>" for address, msg in MESSAGES)
    page_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat</title>
    </head>
    <body>
        <form action="/" method="POST">
            <input type="text" id="message" name="message">
            <input type="submit" value="Send">
        </form>
        <div id="messages">
            {messages_html}
        </div>
    </body>
    </html>
    """
    response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: keep-alive\r\n\r\n{page_html}"""
    return response

def generate_message(addr, message):
    """
    Generates an HTML snippet for a single message.

    Args:
        addr (str): The address of the sender.
        message (str): The message content.

    Returns:
        str: The HTML snippet as a string.
    """
    response = f"""<p>{addr} : {message}</p>"""
    return response

def handle_client(conn, addr):
    """
    Handles communication with a single client.

    Args:
        conn (socket.socket): The client connection socket.
        addr (tuple): The address of the client.
    """
    print('Connected by', addr)
    CONNECTED_CLIENTS.append(conn)
    print(f"Connected clients: {len(CONNECTED_CLIENTS)}")
    try:
        response = generate_page()
        conn.sendall(response.encode('utf-8'))
        while True:
            resp = conn.recv(1024)
            if not resp:
                break
            resp = resp.decode('utf-8')
            message = " ".join(resp.split('\r\n')[-1].split('=')[-1].split('+'))
            if message:
                MESSAGES.append((addr[0], message))
                response = generate_message(addr[0], message)
                for client in CONNECTED_CLIENTS:
                    try:
                        client.sendall(response.encode('utf-8'))
                    except Exception as e:
                        print(f"Error sending message to client: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        CONNECTED_CLIENTS.remove(conn)
        print(f"Disconnected by {addr}")
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

if __name__ == "__main__":
    start_server()