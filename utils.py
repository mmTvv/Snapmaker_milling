import serial, time
from threading import Thread 
import sys 

class Utils(object):
	def __init__(self):
		self.ard = serial.Serial('COM3', 115200)	
		self.snap = serial.Serial('COM10', 115200)
		self.actual_z = [   [],
							[],
							[],
							[],
							[],
							[],
							[],
							[],
							[],
							[],
						]

	def ard_send(self, data):
		self.ard.write(str(data).encode('utf-8'))

	def ard_read(self):
		data = self.ard.read().decode('utf-8')
		if data == '8':
			self.snap.write("M112\r\n".encode('utf-8'))
			sys.exit(0)

		else:
			return data

	def to_right(self):
		time.sleep(1)
		self.snap.write(('G53 G0 Z60 F1500\r\n').encode("utf-8"))
		time.sleep(1)
		self.snap.write("G91\r\n".encode('utf-8'))
		time.sleep(1)
		self.snap.write("G0 X10 F1500\r\n".encode('utf-8'))
		time.sleep(1)
		self.snap.write("G90\r\n".encode('utf-8'))
		time.sleep(1)

	def to_left_to_home(self):
		time.sleep(1)
		self.snap.write(('G53 G0 X25 F1500\r\n').encode("utf-8"))
		time.sleep(2)
		self.snap.write("G91\r\n".encode('utf-8'))
		time.sleep(2)
		self.snap.write("G0 Y10 F1500\r\n".encode('utf-8'))
		time.sleep(2)
		self.snap.write("G90\r\n".encode('utf-8'))

	def home(self):
		#self.snap.write(('G53\r\n').encode('utf-8'))
		#self.snap.write(("G28\r\n").encode("utf-8"))
		self.snap.write(('G53 G0 X25 F1500\r\n').encode("utf-8"))
		self.snap.readline().decode('utf-8')

		time.sleep(5)

		self.snap.write(('G53 G0 Y20 F1500\r\n').encode("utf-8"))
		self.snap.readline().decode('utf-8')

		time.sleep(5)

		self.snap.write(('G53 G0 Z60 F1500\r\n').encode("utf-8"))
		self.snap.readline().decode('utf-8')
		time.sleep(5)
	
	def cord(self):
		self.snap.write(('M114\r\n').encode("utf-8"))

		a = (self.snap.readline().decode('utf-8'))
		b = (self.snap.readline().decode('utf-8'))
		if 'X' in a:
			return a.replace('\n', '').split()
		elif 'X' in b:
			return b.replace('\n', '').split()
		else:
			return self.cord()

	def check_Z(self):
		self.snap.write(('G53 G0 Z54 F1500\r\n').encode("utf-8"))
		while True:
			self.ard_send(1)
			data = self.ard_read()

			if data == '1':
				z = self.cord()
				return z
			

			time.sleep(0.05)
			self.snap.write(('G91\r\n').encode("utf-8"))
			self.snap.readline()
			self.snap.write(('G0 Z-0.01 F1500\r\n').encode("utf-8"))
			self.snap.readline()
			self.snap.write(('G90\r\n').encode("utf-8"))
			self.snap.readline()
