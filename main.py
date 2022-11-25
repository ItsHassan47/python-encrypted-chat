import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input('Do you want to host (1) or connect (2): ')

if choice == '1':
    # for TCP socket.SOCK_STEAM and for UDP SOCK_DGRAM
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.18.42', 7777))    # bind IPv4 and port
    server.listen()
    client, _ = server.accept()
    client.send(public_key.save_pkcs1('PEM'))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == '2':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.18.42', 7777))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1('PEM'))
else:
    exit()


def sending_messages(c):
    while True:
        message = input('')
        c.send(rsa.encrypt(message.encode(), public_partner))
        print(f'You: {message}')


def receiving_messages(c):
    while True:
        print(f'Partner: {rsa.decrypt(c.recv(1024), private_key).decode()}')


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
