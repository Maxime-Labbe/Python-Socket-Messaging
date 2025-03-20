def generate_page(messages):
    """
    Generates the HTML page with the current messages.

    Returns:
        str: The HTML page as a string.
    """
    messages_html = "".join(f"<p>User {user} : {msg}</p>" if not("<p>" in msg) else msg for user, msg in messages)
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

def generate_message(user, message):
    """
    Generates an HTML snippet for a single message.

    Args:
        addr (str): The address of the sender.
        message (str): The message content.

    Returns:
        str: The HTML snippet as a string.
    """
    response = f"""<p>User {user} : {message}</p>"""
    return response

def generate_message_user_connection(addr,user):
    """
    Generates an HTML snippet for a user connection message.

    Args:
        addr (str): The address of the sender.

    Returns:
        str: The HTML snippet as a string.
    """
    response = f"""<p>New user connected from {addr} as User {user}</p>"""
    return response

def generate_message_user_disconnection(addr,user):
    """
    Generates an HTML snippet for a user disconnection message.

    Args:
        addr (str): The address of the sender.

    Returns:
        str: The HTML snippet as a string.
    """
    response = f"""<p>User {user} disconnected from {addr}</p>"""
    return response