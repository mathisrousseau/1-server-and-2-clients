# -*-coding:Latin-1 -*
import socket
import time
import timeit

connection = True
LOG_INTERVAL = 10
lastLog = timeit.default_timer()
#We begin with one message
nb_msg = 1

latency = []
latency_sent = []

#Creation of the client
co_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connection with the serveur
co_client.connect(('localhost', 12800))

msg_sent = ""

while connection != False:
    try:
        msg_sent = "frame"
        #Start
        startTime = timeit.default_timer()
        #print("The start time is : {}".format(startTime))

        logDiffTime = startTime - lastLog
        #print("logDiffTime is : {}".format(logDiffTime))

        if logDiffTime < LOG_INTERVAL:
            co_client.send(msg_sent.encode())
            nb_msg += 1

            ack_server = co_client.recv(1024)
            #print(ack_server.decode())
    
            #End
            endTime = timeit.default_timer()
            #print("The end time is : {}".format(endTime))
    
            #Total time
            totalTime = endTime - startTime
            #print("Total time is : {}".format(totalTime))
            latency.append(totalTime)
    
        elif logDiffTime > LOG_INTERVAL:
            lastLog = startTime
            latency_sent = latency
            co_client.send((msg_sent+'/'+str(latency_sent)).encode())
            latency = []
            ack_server = co_client.recv(1024)
            print("logging")
            #print("lasLog time is now : {}".format(lastLog))
            print("There was/were {} message(s) sent.".format(nb_msg))
            nb_msg = 0

        time.sleep(1)
    
        #We send this time to the server
        #co_client.send(str(totalTime).encode())

    except KeyboardInterrupt :
        break


print("End of the connection")
co_client.close()
