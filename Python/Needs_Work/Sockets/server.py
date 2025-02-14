import socket
import time
import os

os.system('cls') 
s = socket.socket()         
print ("Socket successfully created")
port = 12345               
s.bind(('', port))         
print ("socket binded to %s" %(port)) 
 
s.listen(5)     
print ("socket is listening")
while True: 
  c, addr = s.accept()     
  print ('Got connection from', addr )
  c.send('Thank you for connecting'.encode()) 

  running = True
  counter = 0
  while running:
    c.send(f'{counter}'.encode()) 
    counter += 1
    time.sleep(1.0)
 
  c.close()
  break
