import pygame
import os

os.system("cls")

screen_x = 1280
screen_y = 720

icon = pygame.image.load('icon.png')
screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
pygame.display.set_caption("UI Builder")
pygame.display.set_icon(icon)

testing = True
green = (0, 255, 150)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
grey = (150, 150, 150)
black = (0,0,0)

class button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = False
    
    def draw(self):
        pygame.draw.rect(screen, black, pygame.Rect(self.x, self.y, self.width, self.height))
        if self.selected:
            pygame.draw.rect(screen, white, pygame.Rect(self.x+5, self.y+5, self.width-10, self.height-10))
        else:
            pygame.draw.rect(screen, grey, pygame.Rect(self.x+5, self.y+5, self.width-10, self.height-10))
        if testing:
            range_of_error = 10
            top_left = (self.x, self.y)
            top_right = (self.x+self.width, self.y)
            bottom_left = (self.x, self.y+self.height)
            bottom_right = (self.x+self.width, self.y+self.height)
            top_edge = pygame.Rect(self.x-range_of_error, self.y-range_of_error, self.width, 2*range_of_error)
            corner_array = [top_left, top_right, bottom_left, bottom_right]
            for corner in corner_array:
                cx = corner[0]
                cy = corner[1]
                corner_rect = pygame.Rect(cx-range_of_error, cy-range_of_error, 2*range_of_error, 2*range_of_error)
                pygame.draw.rect(screen, red, corner_rect)
            pygame.draw.rect(screen, blue, top_edge)

    def correct(self):
        screen_x = screen.get_size()[0]
        screen_y = screen.get_size()[1]
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        if self.x > screen_x: self.x = screen_x
        if self.y > screen_y: self.y = screen_y
        if self.width < 5: self.width = 5
        if self.height < 5: self.height = 5
        if self.width+self.x > screen_x: self.width = screen_x-self.x
        if self.height+self.y > screen_y: self.height = screen_y-self.y

    def check_clicked(self):
        bottom = self.y+self.height
        right = self.x+self.width
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > self.x and mouse_pos[0] < right:
            if mouse_pos[1] > self.y and mouse_pos[1] < bottom:
                self.selected = True
                print(self.text, self.selected)

    def move_buttons(self):
        global dragging, count
        range_of_error = 10
        mouse_pos = pygame.mouse.get_pos()
        # corners
        top_left = (self.x, self.y)
        top_right = (self.x+self.width, self.y)
        bottom_left = (self.x, self.y+self.height)
        bottom_right = (self.x+self.width, self.y+self.height)
        corner_array = [top_left, top_right, bottom_left, bottom_right]
        if not dragging:
            count = 0 
        os.system('cls')
        for corner in corner_array:
            cx = corner[0]
            cy = corner[1]
            corner_rect = pygame.Rect(cx-range_of_error, cy-range_of_error, 2*range_of_error, 2*range_of_error)
            if self.selected:
                if (mouse_pos[0] > cx-range_of_error and mouse_pos[0] < cx+range_of_error) or dragging:
                    if (mouse_pos[1] > cy-range_of_error and mouse_pos[1] < cy+range_of_error) or dragging:      
                        dragging = True
                        if count == 0:      
                            self.x = mouse_pos[0]
                            self.y = mouse_pos[1]
                        if count == 1:
                            self.width = mouse_pos[0]-self.x
                        if count == 2:
                            self.height = mouse_pos[1]-self.y
                        if count == 3:
                            self.width = mouse_pos[0]-self.x
                            self.height = mouse_pos[1]-self.y
                        #pygame.draw.rect(screen, red, corner_rect)
                        self.correct()
                if not dragging:
                    count += 1


def draw_buttons():
    for i in button_array:
        i.draw()

def check_buttons():
    os.system('cls')
    for i in button_array:
        i.selected = False
        i.check_clicked()

def size_buttons():
    for i in button_array:
        i.move_buttons()

button_array = []
button_array.append(button(10, 10, 300, 300, "button #1"))
flag = ""
dragging = False
count = 0

screen.fill(green)
running = True
while running:
    flag = ""
    screen.fill(green)
    draw_buttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3)[0]:
                check_buttons()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                button_array.append(button(10, 10, 200, 200, f"button #{len(button_array)+1}"))
            if event.key == pygame.K_z and len(button_array) > 0:
                button_array.pop()
    if pygame.mouse.get_pressed(3)[2]:
        screen.fill(green)
        draw_buttons()
        size_buttons()
    if not pygame.mouse.get_pressed(3)[2]:
        dragging = False
    if flag != "":
        print(flag)
    pygame.display.update()
