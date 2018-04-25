import socket
import time
import timeit

connection = True

hote = ''
port_1 = 12800
port_2 = 12801

latency_1 = [] #Client_1
latency_2 = [] #Server
latency_3 = [] #Client_2

#For the client_1
connection_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#For the client_2
connection_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connection with client_1
connection_1.bind((hote, port_1))
#Connection with client_2
connection_2.bind((hote, port_2))

connection_1.listen(5)
connection_2.listen(5)
print("The server listens the port {} of client_1".format(port_1))
print("The server listens the port {} of client_2".format(port_2))

connection_with_client_1, infos_connection_1 = connection_1.accept()
print("Client 1 is connected : {}".format(infos_connection_1))
connection_with_client_2, infos_connection_2 = connection_2.accept()
print("Client 2 is connected : {}".format(infos_connection_2))


while connection != False:
    try:
        msg_recv_1 = connection_with_client_1.recv(1024)
        print("Message of the client_1 : {}".format(msg_recv_1.decode()))
        msg_recv_1 = msg_recv_1.decode()
        connection_with_client_1.send(b"5 / 5")

        a = msg_recv_1.find("/")
        if a != -1:
            frame = msg_recv_1[:a]
            latency_1.append(msg_recv_1[a+1:])

        #v_1 Latency_1
        #latency_client_1 = connection_with_client_1.recv(1024)
        #latency_1.append(latency_client_1.decode())

        #Latency_2
        #There is not process, so no latency
        latency_2.append(0)
    
        #Latency_3
        startTime = timeit.default_timer()
        connection_with_client_2.send(b"Command")
        msg_recv_2 = connection_with_client_2.recv(1024)
        endTime = timeit.default_timer()
        print("Message of the client_2 : {}".format(msg_recv_2.decode()))
        totalTime = endTime - startTime
        print("Total time for client_2 is : {}".format(totalTime))
        latency_3.append(totalTime)

    except socket.error :
        break

    except KeyboardInterrupt :
        break

#connexion_avec_client_1.send(b"5 / 5")
connection_with_client_2.send(b"fin")
print("End of the connection")

print("List of the client_1's latency: {}".format(latency_1))

print("List of the server's latency: {}".format(latency_2))

print("List of the client_2's latency: {}".format(latency_3))

connection_with_client_1.close()
connection_with_client_2.close()
connection_1.close()
connection_2.close()
