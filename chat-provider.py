import socket
import threading

# Server setup
HOST = '127.0.0.1'  # localhost
PORT = 5555         # Port to listen on

# List to hold all connected client sockets
clients = []

def broadcast_message(message, sender_socket):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # If sending fails, close connection and remove client
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """Handle communication with a single client."""
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received: {message.decode('utf-8')}")
            broadcast_message(message, client_socket)
        except:
            # Handle disconnect
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    """Start the chat server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Listen for connections

    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
