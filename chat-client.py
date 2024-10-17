import socket
import threading

HOST = '127.0.0.1'  # localhost
PORT = 5555

def receive_messages(client_socket):
    """Continuously receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}")
        except:
            print("Connection closed by server.")
            client_socket.close()
            break

def send_messages(client_socket):
    """Continuously send messages to the server."""
    while True:
        message = input("")
        client_socket.send(message.encode('utf-8'))

def start_client():
    """Start the chat client."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Start threads for receiving and sending messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    threading.Thread(target=send_messages, args=(client_socket,)).start()

if __name__ == "__main__":
    start_client()
