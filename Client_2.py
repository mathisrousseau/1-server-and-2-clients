import socket
import time

#Creation of the client
co_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connection with the server
co_client.connect(('localhost', 12801))

print("Connected to the server")

#Message received from the server
msg_server = co_client.recv(1024)

#Envoie de l'accuse de reception
while msg_server == b"Command":
    
    print("Message of the server : {}" \
        .format(msg_server.decode()))

    co_client.send(b"OK")

    msg_server = co_client.recv(1024)   

print("Closing socket")
co_client.close()
