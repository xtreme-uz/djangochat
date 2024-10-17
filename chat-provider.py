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

def send_private_message(receiver_socket, message):
    """Send a private message to a specific user."""
    try:
        receiver_socket.send(f"Private: {message}".encode('utf-8'))
    except:
        receiver_socket.close()
        clients.remove(receiver_socket)

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
            
            # Check if the message is a private message (starts with @username)
            if message.startswith('@'):
                recipient_name, private_message = message.split(' ', 1)
                recipient_name = recipient_name[1:]  # Remove the '@'

                recipient_socket = None
                for client, user in usernames.items():
                    if user == recipient_name:
                        recipient_socket = client
                        break
                
                if recipient_socket:
                    private_msg = f"{usernames[client_socket]} (private): {private_message}"
                    send_private_message(recipient_socket, private_msg)
                else:
                    client_socket.send(f"User {recipient_name} not found.".encode('utf-8'))
            else:
                # Otherwise, broadcast the message to all clients
                formatted_message = f"{usernames[client_socket]}: {message}"
                print(formatted_message)
                broadcast_message(formatted_message, client_socket)
    except:
        pass
    finally:
        # Remove client and notify others
        clients.remove(client_socket)
        leave_message = f"{usernames[client_socket]} has left the chat."
        print(leave_message)
        broadcast_message(leave_message)
        del usernames[client_socket]
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
