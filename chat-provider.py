import socket
import threading

# Server setup
HOST = '127.0.0.1'  # localhost
PORT = 5555         # Port to listen on

clients = []
usernames = {}

def broadcast_message(message, sender_socket=None):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """Handle communication with a single client."""
    try:
        # Ask for a username and announce it to the chat
        client_socket.send("Enter your username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        welcome_message = f"{username} has joined the chat!"
        print(welcome_message)
        broadcast_message(welcome_message, client_socket)
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            formatted_message = f"{username}: {message}"
            print(formatted_message)
            broadcast_message(formatted_message, client_socket)
    except:
        pass
    finally:
        # Remove client and notify others
        clients.remove(client_socket)
        leave_message = f"{username} has left the chat."
        print(leave_message)
        broadcast_message(leave_message)
        client_socket.close()

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
