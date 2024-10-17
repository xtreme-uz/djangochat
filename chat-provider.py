import socket
import threading

# Server setup
HOST = '127.0.0.1'  # localhost
PORT = 5555         # Port to listen on

clients = {}  # Maps client sockets to their info (username, current room)
rooms = {}    # Maps room names to a list of client sockets

def broadcast_message(message, room, sender_socket=None):
    """Send a message to all clients in the same room except the sender."""
    for client in rooms.get(room, []):
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                rooms[room].remove(client)

def send_private_message(receiver_socket, message):
    """Send a private message to a specific user."""
    try:
        receiver_socket.send(f"Private: {message}".encode('utf-8'))
    except:
        receiver_socket.close()
        for room in rooms.values():
            if receiver_socket in room:
                room.remove(receiver_socket)

def handle_client(client_socket):
    """Handle communication with a single client."""
    try:
        # Ask for a username
        client_socket.send("Enter your username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = {"username": username, "room": None}

        # Handle room selection
        while True:
            client_socket.send("Enter a room name to join or create: ".encode('utf-8'))
            room_name = client_socket.recv(1024).decode('utf-8')

            if room_name not in rooms:
                rooms[room_name] = []
            
            # Add client to the selected room
            rooms[room_name].append(client_socket)
            clients[client_socket]["room"] = room_name
            welcome_message = f"{username} has joined {room_name}!"
            broadcast_message(welcome_message, room_name, client_socket)
            client_socket.send(f"You are now in room: {room_name}".encode('utf-8'))
            break

        # Message handling within the room
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # Private message check (starts with @username)
            if message.startswith('@'):
                recipient_name, private_message = message.split(' ', 1)
                recipient_name = recipient_name[1:]  # Remove the '@'

                recipient_socket = None
                for client, info in clients.items():
                    if info["username"] == recipient_name and info["room"] == clients[client_socket]["room"]:
                        recipient_socket = client
                        break
                
                if recipient_socket:
                    private_msg = f"{clients[client_socket]['username']} (private): {private_message}"
                    send_private_message(recipient_socket, private_msg)
                else:
                    client_socket.send(f"User {recipient_name} not found in this room.".encode('utf-8'))
            elif message.startswith('/switch'):
                # Switch room logic
                new_room = message.split(' ')[1]
                if new_room not in rooms:
                    rooms[new_room] = []

                # Leave the current room
                current_room = clients[client_socket]["room"]
                rooms[current_room].remove(client_socket)
                broadcast_message(f"{clients[client_socket]['username']} has left the room.", current_room)

                # Join the new room
                rooms[new_room].append(client_socket)
                clients[client_socket]["room"] = new_room
                broadcast_message(f"{clients[client_socket]['username']} has joined the room.", new_room)
                client_socket.send(f"You have switched to room: {new_room}".encode('utf-8'))
            else:
                # Broadcast the message to the current room
                current_room = clients[client_socket]["room"]
                formatted_message = f"{clients[client_socket]['username']}: {message}"
                broadcast_message(formatted_message, current_room, client_socket)
    except:
        pass
    finally:
        # Remove client and notify others
        if client_socket in clients:
            room = clients[client_socket]["room"]
            if room and client_socket in rooms.get(room, []):
                rooms[room].remove(client_socket)
                broadcast_message(f"{clients[client_socket]['username']} has left the chat.", room)
            del clients[client_socket]
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
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
