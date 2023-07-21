import threading
import socket

users = input('Choose a username: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.30.200.144', 59000))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "user?":
                client.send(users.encode('utf-8'))
            else:
                print(message)
        except:
            print('Goodbye!')
            client.close()
            break

def client_send():
    while True:
        message = input("")
        if message.strip().lower() == 'bye':
            client.send("bye".encode('utf-8'))
            client.close()
            break
        client.send(f'{users}: {message}'.encode('utf-8'))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
