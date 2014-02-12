#!/usr/bin/env python

#Sample Code by: Muhammad Adnan Aftab
#This is sample python code to show how to sniff packet and decode it
#This code using raw socket to sniff packet whcih operates on network layer 2
#Any body can use this code free of charge and can extend it. 
#No warranty at all.

import socket
import struct
import binascii

rawSocket = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))

pkt = rawSocket.recvfrom(2048)
ethernetHeader = pkt[0][0:14]

# Unpacking ethernet header (first 14 byets)
eth_hdr = struct.unpack("!6s6s2s",ethernetHeader)
print "Source Mac address : ",binascii.hexlify(eth_hdr[0])
print "Destination mac : ",binascii.hexlify(eth_hdr[1])
print "EthType(inner type) : ",binascii.hexlify(eth_hdr[2])

#Unpacking IP header 20 bytes from 14
ipHeader = pkt[0][14:34]
ip_hdr = struct.unpack("!12s4s4s",ipHeader)
print "Source IP address "+socket.inet_ntoa(ip_hdr[1])
print "Destination IP address "+socket.inet_ntoa(ip_hdr[2])

#Unpacking TCP header
tcpHeader = pkt[0][34:54]
tcp_hdr = struct.unpack("!HH16s",tcpHeader)
print "Source port : "+str(tcp_hdr[0])
print "Destination port : "+str(tcp_hdr[1])
print "Data : "+binascii(tcp_hdr[2])




