# Local messaging server

This project allows you to message someone on your local network via a website interface.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Warning](#warning)

## Installation

### Prerequisites

- Python 3.x

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/Maxime-Labbe/Python-Socket-Messaging.git
    cd Python-Socket-Messaging
    ```

2. Configure the host and the port:

    ```python
    HOST = '' # Change this to your local IP address
    PORT =  # Change this to your desired port
    ```

3. Open your port in your firewall:

    - Go to your machine firewall
    - Add the port to your firewall
    - Open only for private network

4. Start the server:

    ```bash
    python socket_server.py
    ```

5. Open your browser and navigate to `http://HOST:PORT` on any devices (there might be issue using with a phone) from your network.

## Usage

### Sending messages

- Enter your message and send it.
- Now you can see the message on each device that is connected and from which device it comes from.

## Project Structure

```bash
Python-Socket-Messaging/
├── socket_server.py
└── README.md
```

## Warning

There is no security features on this app which makes it probably very simple to hack. Thus I recommend to anyone who might want to use it to do it on a private and safe network.