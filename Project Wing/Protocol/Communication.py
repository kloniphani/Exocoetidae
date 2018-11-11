"""         
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       January 22, 2018
Copyrights:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
"""
import socket, sys
import datetime, time

from numpy import *
from multiprocessing import Process
from threading import Thread

#Object Orinted File: Local Source
from GUI.Interface import * 

class Communication(object):
	"""description of class"""
	pass


class Socket(Thread):
	"""description of class"""
	def __init__(self, Socket = None):
		Thread.__init__(self)
		if Socket is None:
			self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		else:
			self.Socket = Socket

	def __init__(self, Host = None, Port = None, Socket = None, Results = False):
		Thread.__init__(self)
		if Socket is None:
			self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		else:
			self.Socket = Socket

		if Host is not None and Port is not None:
			self.Bind(Host, Port, Results)

	def Bind(self, Host, Port, Results = False):
		self.Host = Host; self.Port = Port;
		try:
			self.Socket.bind((Host, Port))
			if Results is True: print('$ Binded \'{}\':{}'.format(Host, Port));
		except:
			print('! Connecting Error: {}\t{}'.format(self.Socket.getsockname(), sys.exc_info()))
			sys.exit(1)

	def Connect(self, Host, Port, Results = False):
		if int(Port) == int(self.Socket.getsockname()[1]) and Host == self.Socket.getsockname()[0]:
			return False
		else:
			try:
				self.Socket.connect((Host, Port))
				if Results is True: print('$ {} Connected to {}'.format(self.Socket.getsockname(), (Host, Port)));
				return True
			except:
				if Results is True:
				   print('! Connecting Error - From: {} To: {}\t{}'.format(self.Socket.getsockname(), (Host, Port), sys.exc_info()[1]))
				return False

	def Close(self, Results = False):
		try:
			self.Socket.close()
			self.Bind(self.Host, self.Port, Results)
			if Results is True: print('$ Socket: {} Closed'.format(self.Socket.getsockname()));
		except:
			print('! Closing Error: {}\t{}'.format(self.Socket.getsockname(), sys.exc_info()))

	def Send(self, Message, Results = True):
		try:
			self.Socket.sendall(Message.encode('utf-8'))
			if Results is True: print('$ Message - {} - Successfully Sent'.format(Message));
		except:
			print('! Sending Error: {}\t{}'.format(self.Socket.getsockname(), sys.exc_info()))

	def SendTo(self, Host, Port, Message, Results = True):
		try:
			Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			Socket.connect((Host, Port))
			Socket.send(Message.encode('utf-8'))
			if Results is True: 
				print('$ Message - {} - Successfully Sent to: {}'.format(Message, (Host, Port)));
				Message = Socket.recv(1024).decode('utf-8')
				print(Message)
			Socket.close()
		except:
			print('! Sending Error: {}\t{}'.format(self.Socket.getsockname(), sys.exc_info()))

	def _SendTo(Host, Port, Message, Results = True):
		try:
			Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			Socket.connect((Host, Port))
			Socket.send(Message.encode('utf-8'))
			if Results is True: print('$ Message - {} - Successfully Sent'.format(Message));
			Socket.close()
		except:
			print('! Sending Error: {}\t{}'.format(self.Socket.getsockname(), sys.exc_info()))

	def Recieve(self, Results = False):
		Message = ''
		try:			
			while True:
				Data = self.Socket.recv(1024).decode('utf-8')
				if not Data: break
				Message += Data
			if Results is True: print('$ Message - {} - Successfully Received'.format(Message));
			return Message
		except:
			print('! Recieving Error: {}\t{}'.format(self.Socket.getsockname(), sys.exc_info()[1]))

	def Connection(self, ConnectedClient, Address, Results = False):
		if Results is True:
			ConnectedClient.send('$ {} Successfully Connected to: {} and Recieving Data Through The open Connection'.format(self.Socket.getsockname(), Address).encode('utf-8'))

		#Console = Interface(Title = 'Server Connection: {}'.format(self.Socket.getsockname()))
		#Console.OutputConsoleWidget()
		
		while True:
			Message = ConnectedClient.recv(1024).decode('utf-8')
			if not Message: break;
			#Console.Insert(Message = 'From: {}\t'.format(Address) + str(Message))
			
		ConnectedClient.close()

	def Listen(self, LifeTime = 2, Size = 1, Results = False):
		try:
			self.Socket.listen(Size)
			Start = datetime.datetime.now()
			if Results is True: print('$ Listening for Connection on Socket: {}\t\tTime: {}'.format(self.Socket.getsockname(), Start))

			while True:
				try:
					ConnectedClient, ConnectedAddress = self.Socket.accept()
					if Results is True: print('$ {} Accepted Connection from: {}\t\tTime: {}'.format(self.Socket.getsockname(), ConnectedAddress, datetime.datetime.now()));	

					#Starting a Connection Thread for multiple communication
					Thread(target = self.Connection, args = (ConnectedClient, ConnectedAddress, True,)).start()
					
					
					Count = datetime.datetime.now() - Start
					datetime.timedelta(0, 8, 562000)
					if int(divmod(Count.days * 86400 + Count.seconds, 60)[0]) > LifeTime:
						print('! Time Up ----- END')
						break
				except socket.timeout:
					print('! Connection \'Timeout\' Error: {}\t{}'.format(self.Socket.getsockname(), sys.exc_info()[1]))
					continue
				except: 
					print('! Connection Error: {} - - - {}\n\t{}'.format(self.Socket.getsockname(), ConnectedAddress, sys.exc_info()))	
					continue
				
			self.Close(Results = Results)
			return True
		except:
			print('! Listening Error: {} - - - {}\n\t{}'.format(self.Socket.getsockname(), ConnectedAddress, sys.exc_info()))
			return False
			
class Message(object):
	"""description of class"""
	pass

if __name__ is '__main__':
	from time import sleep

	SOCKETS = [] 
	Low = 40000; High = 40005; #Port range

	for port in range(Low, High):
		sock = Socket(socket.gethostbyname(socket.gethostname()), port, None, True) #Using an Ip Address (xxx.xxx.xxx.xxx)
		SOCKETS.append(sock)
		del sock

	for sock in SOCKETS:
		Thread(target = sock.Listen, args = (5, 100, True,)).start()

	sleep(1)

	#Send random message to random ports using Threads
	for loop in range(2):
		Sender = random.choice(range(len(SOCKETS)))
		Reciever = random.randint(Low, High)
		
		T = Thread(target = SOCKETS[Sender].SendTo, args = (socket.gethostbyname(socket.gethostname()), Reciever, "Test for Communication",)) #Using an Ip Address (xxx.xxx.xxx.xxx)
		T.start()

	sleep(30)