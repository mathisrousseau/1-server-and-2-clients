import os
import socket
import time
import timeit
import csv

os.chdir("C:\\Users\\Rousseau\\Desktop\\Python\\latency_with_timeit")
#CSV document
w_file=open('test.csv', 'w')
writeCSV = csv.writer(w_file, delimiter=';', lineterminator='\n')

connection = True
frame = "frame"

hote = ''
port_1 = 12800
port_2 = 12801

#Client_1
latency_1 = [] 
latency_1_csv = []
latency_1_avg = []
avg_1 = 0
min_1 = []
max_1 = []
minLat_1 = 1
maxLat_1 = 0

#Server
latency_2 = []
latency_2_avg = []
avg_2 = 0
min_2 = []
max_2 = []
minLat_2 = 1
maxLat_2 = 0

#Client_2
latency_3 = []
latency_3_avg = []
avg_3 = 0
min_3 = []
max_3 = []
minLat_3 = 1
maxLat_3 = 0

#Latency end-to-end
latency_e2e = []
min_e2e = []
max_e2e = []

timestamp = []
nb_msg = []

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
        #print("Message of the client_1 : {}".format(msg_recv_1.decode()))
        msg_recv_1 = msg_recv_1.decode()
        connection_with_client_1.send(b"5 / 5")

        a = msg_recv_1.find("L")
        b = msg_recv_1.find("T")
        c = msg_recv_1.find("V")
        if a != -1:
            frame = msg_recv_1[:a]
            latency_1.append(msg_recv_1[a+1:b])
            timestamp.append(float(msg_recv_1[b+1:c]))
            nb_msg.append(int(msg_recv_1[c+1:]))

        if msg_recv_1 and frame == "frame":
            #Latency_2
            #There is not process, so no latency
            latency_2.append(0)
        
            #Latency_3
                #Start time
            startTime = timeit.default_timer()
            connection_with_client_2.send(b"Command")
            msg_recv_2 = connection_with_client_2.recv(1024)
                #End time
            endTime = timeit.default_timer()

            #print("Message of the client_2 : {}".format(msg_recv_2.decode()))

                #Total time
            totalTime = endTime - startTime
            #print("Total time for client_2 is : {}".format(totalTime))
            latency_3.append(totalTime)

    except socket.error :
        break

    except KeyboardInterrupt :
        break

#connection_with_client_1.send(b"5 / 5")
connection_with_client_2.send(b"fin")

#Convertion of values in the latency_1 into float
i=0
for i in range(len(latency_1)):
    d = latency_1[i].find("[")
    e = latency_1[i].find("]")

    if d!=-1 and e!=-1:
        latency_1[i] = latency_1[i][d+1:e]

        latency_1[i] = latency_1[i].split(" ")
        
        j=0
        for j in range(len(latency_1[i])):
            f = latency_1[i][j].find(",")
            if f!=-1:
                latency_1[i][j] = latency_1[i][j][:f]
                latency_1_csv.append(float(latency_1[i][j]))
                
            else:
                latency_1_csv.append(float(latency_1[i][j]))

#Add a fake value at the end of the latency_1_csv
latency_1_csv.append(0.009)

#print("List of the client_1's latency: {}\n".format(latency_1))

#print("LATENCY_1_TEMP: {}\n{}".format(latency_1_csv,type(latency_1_csv[0])))

#print("List of the server's latency: {}\n".format(latency_2))

#print("List of the client_2's latency: {}\n".format(latency_3))

#print("List of the timestamps : {}\n".format(timestamp))

#print("List of the number of messages sent : {}\n".format(nb_msg))

#Average, Min and Max // Create a function !!
s = 0
p = 0
#for s in range(len(latency_1_csv)):
while s <= nb_msg[p]:
    #Average
    avg_1 += latency_1_csv[s]
    avg_2 += latency_2[s]
    avg_3 += latency_3[s]

    #Client_1
    if (latency_1_csv[s] < minLat_1):
        minLat_1 = latency_1_csv[s]
    if (latency_1_csv[s] > maxLat_1):
        maxLat_1 = latency_1_csv[s]

    #Server    
    if (latency_2[s] < minLat_2):
        minLat_2 = latency_2[s]
    if (latency_2[s] > maxLat_2):
        maxLat_2 = latency_2[s]
        
    #Client_2    
    if (latency_3[s] < minLat_3):
        minLat_3 = latency_3[s]
    if (latency_3[s] > maxLat_3):      
        maxLat_3 = latency_3[s]

    s += 1

    if s == nb_msg[p]:
        #Client_1
        avg_1 = avg_1/nb_msg[p]
        latency_1_avg.append(avg_1)
        min_1.append(minLat_1)
        max_1.append(maxLat_1)

        #Client_2
        avg_2 = avg_2/nb_msg[p]
        latency_2_avg.append(avg_2)
        min_2.append(minLat_2)
        max_2.append(maxLat_2)
        
        #Client_3
        avg_3 = avg_3/nb_msg[p]
        latency_3_avg.append(avg_3)
        min_3.append(minLat_3)
        max_3.append(maxLat_3)
        
        del latency_1_csv[:nb_msg[p]]
        #print("new latency_1_csv:{}\n"\
         #   "Its length : {}".format(latency_1_csv,len(latency_1_csv)))
            
        del latency_2[:nb_msg[p]]
        del latency_3[:nb_msg[p]]
        avg_1, avg_2, avg_3 = 0,0,0
        minLat_1, minLat_2, minLat_3 = 1,1,1
        maxLat_1, maxLat_2, maxLat_3 = 0,0,0
        
        s = 0
        p +=1
        if latency_1_csv == []:
            break

#Latency e2e
for n in range(len(latency_1_avg)):
    #Avg
    latency_e2e.append((latency_1_avg[n]+latency_2_avg[n]+ latency_3_avg[n])/3)
    #Min
    min_e2e.append((min_1[n]+min_2[n]+min_3[n])/2)
    #Max
    max_e2e.append((max_1[n]+max_2[n]+max_3[n])/2)

writeCSV.writerow(["timestamp (s)", "Nb values sent", \
                   "lat_1_avg (s)", "lat_1_min", "lat_1_max", \
                   "lat_2_avg (s)", "lat_2_min", "lat_2_max",\
                   "lat_3_avg (s)", "lat_3_min", "lat_3_max", \
                   "lat_e2e_avg (s)", "lat_e2e_min", "lat_e2e_max"])

for k in range(len(nb_msg)):
    writeCSV.writerow([str(timestamp[k])[:10], str(nb_msg[k]),\
                      str(latency_1_avg[k])[:10], str(min_1[k])[:10], \
                           str(max_1[k])[:10], \
                      str(latency_2_avg[k]), str(min_2[k]), \
                           str(max_2[k])[:10], \
                      str(latency_3_avg[k])[:10], str(min_3[k])[:10], \
                           str(max_3[k])[:10], \
                      str(latency_e2e[k])[:10], str(min_e2e[k])[:10], \
                           str(max_e2e[k])[:10]])
 
w_file.close()
del c
del w_file

print("End of the connection")
connection_with_client_1.close()
connection_with_client_2.close()
connection_1.close()
connection_2.close()
