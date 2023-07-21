import threading
import socket
import queue

host = ''
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
users = []
blocked_clients = []

client_priority = {}  # Dictionary to store client priority levels
message_queue = queue.PriorityQueue()  # Priority queue for storing messages

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if client in blocked_clients:
                client.send("You are blocked and cannot send messages.".encode('utf-8'))
                break  # Exit the loop for blocked clients
            else:
                priority = client_priority[client]
                message_queue.put((priority, message))  # Add message to the priority queue

            if message.decode('utf-8').strip().lower() == 'bye':
                index = clients.index(client)
                user = users[index]
                broadcast(f'{user.decode("utf-8")} has left the chat room!'.encode('utf-8'))
                clients.remove(client)
                users.remove(user)
                break
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user = users[index]
            users.remove(user)
            if client in blocked_clients:
                blocked_clients.remove(client)
            broadcast(f'{user} has left the chat room! '.encode('utf-8'))
            break

def block_client(client):
    blocked_clients.append(client)
    client.send("You have been blocked by the server.".encode('utf-8'))
    client.close()

def send_messages():
    while True:
        priority, message = message_queue.get()
        broadcast(message)

def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        client.send('user?'.encode('utf-8'))
        user = client.recv(1024)
        users.append(user)
        clients.append(client)
        print(f'The user of this client is {user.decode("utf-8")}'.encode('utf-8'))
        broadcast(f'{user.decode("utf-8")} has connected to the chat room'.encode('utf-8'))
        client.send('You are now connected!'.encode('utf-8'))
        client_priority[client] = int(input("Enter priority level for the client: "))  # Set priority level
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

        # Check if the client should be blocked
        block_decision = input("Do you want to block this client? (yes/no): ")
        if block_decision.lower() == 'yes':
            block_client(client)

if __name__ == "__main__":
    send_thread = threading.Thread(target=send_messages)
    send_thread.start()
    receive()
