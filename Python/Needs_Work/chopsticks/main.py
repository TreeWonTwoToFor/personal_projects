import pygame
import os
import time

os.system('cls')

screen = pygame.display.set_mode((400, 600))

bg_color = (25, 100, 50)
black = (0, 0, 0)
white = (255, 255, 255)
select_color = (250, 50, 0)

class hand:
	def __init__(self, x, y, width, select):
		self.x = x
		self.y = y
		self.width = width
		self.select = select
		self.rect = pygame.Rect(self.x, self.y, self.x+self.width, self.y+self.width)

	def draw(self):
		if self.select:
			pygame.draw.circle(screen, select_color, (self.x, self.y), self.width)
		else:
			pygame.draw.circle(screen, black, (self.x, self.y), self.width)
		pygame.draw.circle(screen, white, (self.x, self.y), self.width-5)

hand_array = [hand(100, 50, 50, 0), hand(300, 50, 50, 0), hand(100, 550, 50, 0), hand(300, 550, 50, 1)]

def draw_hands():
	for hand in hand_array:
		hand.draw()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
	screen.fill(bg_color)
	draw_hands()
	pygame.display.update()
