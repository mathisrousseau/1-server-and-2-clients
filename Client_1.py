# -*-coding:Latin-1 -*
import socket
import time
import timeit

connection = True
LOG_INTERVAL = 5
nb_msg = 0

latency = []
latency_sent = []

#Creation of the client
co_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connection with the serveur
co_client.connect(('localhost', 12800))
lastLog = timeit.default_timer()

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
            #The first total time is higher than other total time
            #Because it's linked with the moment when we run the client 2
            totalTime = endTime - startTime
            #print("Total time is : {}".format(totalTime))
            latency.append(totalTime)
    
        elif logDiffTime > LOG_INTERVAL:
            lastLog = startTime
            nb_msg += 1
            
            #Send message with latency
            co_client.send((msg_sent+'L'+str(latency)+\
                'T'+str(startTime)+'V'+str(nb_msg)).encode())

            #Initialization of the latency list
            latency = []
            
            ack_server = co_client.recv(1024)

            #Measure of this latency
            endTime = timeit.default_timer()

            #Total time
            totalTime = endTime - startTime
            latency.append(totalTime)
            
            print("logging")
            #print("lasLog time is now : {}".format(lastLog))
            print("There was/were {} message(s) sent.".format(nb_msg))
            nb_msg = 0

        time.sleep(0.1)

    except KeyboardInterrupt :
        break


print("End of the connection")
co_client.close()
