import os, csv

os.chdir("C:\\Users\\Rousseau\\Desktop\\Python\\latency_with_timeit")

tableau = [['A', 'B', 'C'],[4.0, 1.1, 1.05],[1.0, 0.6, 1.09]]

w_file=open('test.csv', 'w')
 
c = csv.writer(w_file, delimiter=';', lineterminator='\n')
 
for liste in tableau: c.writerow(liste)
 
w_file.close()
del c
del w_file
