#!/usr/bin/env python

#Code by Muhammad Adnan Aftab
#This is sample code to inject packet via a raw socket in python
#Code can be used free and can also be extend as per requirement.
#NO warranty for any part of the code. Used it on your sole responsibility


import socket
import struct

#Create  RawSocket 
rawSocket = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))

#bind rawSocket with interface, on which you want to inject
rawSocket.bind(('eth0',socket.htons(0x0800)))

#construct packet by packing 
#6s6s2s means 6byte string for destination mac address , 6byte string for source mac address and 2byte string for ether type (0x0800 is ip)
packetToInject = struct.pack('!6s6s2s','\xaa\xaa\xaa\xaa\xaa\xaa','\xbb\xbb\xbb\xbb\xbb\xbb','\x08\x00')

#send packet by adding some sample text

rawSocket.send(packetToInject+"This packet is injected by raw socket")

print "How simple is this...!"

#How to test this 
#1. Run tcpdump with following commands 'tcpdump -i eth0 -vv -XX' on terminal
#2. Open an other window and run this script with root. 
	# first change the permission of file by executing this command 'chmod a+x CXPacketInjectorWithRawSocket' (you have to run this command only once)
	# running as root 'sudo ./CXPacketInjectorWithRawSocket.py' OR you can run 'sudo bash' and then './CXPacketInjectorWithRawSocket.py'
#3. After running scrip go back to other terminal, you will see your packet
