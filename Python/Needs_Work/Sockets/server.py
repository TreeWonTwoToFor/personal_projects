import socket
import time
import os
import game.world
import random
import pygame

clock = pygame.time.Clock()

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
  c.send('Thank you for connecting\n\n'.encode()) 

  my_world = game.world.World()
  player = game.world.Entity("#", (2,2))
  my_world.place_object(player)
  running = True
  while running:
    print(c.recv(1024).decode())
    x = random.randint(0,4)
    y = random.randint(0,4)
    game.world.move_entity(my_world, player, (x,y))
    for i in range(5):
      c.send(str(str(my_world.grid[i])+"\n").encode())
    c.send(str("\n").encode())
    clock.tick(10)
 
  c.close()
  break
