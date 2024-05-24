import serial, time
from threading import Thread 
import sys 
import utils

root = utils.Utils() 

root.home()
file = input("Enter cnc file name: ")
cnc = open(file, 'r')
for i in range(10):
	for j in range(10):
		root.actual_z[i].append(root.check_Z()[2].replace("Z:", ""))
		root.to_right()
	
	root.to_left_to_home()


print(root.actual_z)
root.ard.close()
root.snap.close()