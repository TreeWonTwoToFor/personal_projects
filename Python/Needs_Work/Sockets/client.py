# Import socket module 
import socket
import os
import game

os.system('cls')
 
# Create a socket object 
s = socket.socket()         
 
# Define the port on which you want to connect 
port = 12345               
 
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
 
# receive data from the server and decoding to get the string.
while True:
    print(s.recv(1024).decode(), end="")