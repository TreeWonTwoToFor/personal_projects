import time
import os

car_position = "intersectionA"
start_time = time.time()

# basic functions to handle simulation space
def create_array(x, y, filler):
    cols, rows = (x, y)
    return([[filler for i in range(cols)] for j in range(rows)])

def print_space(space):
    for row in space:
        printed_row = ""
        for square in row:
            printed_row = printed_row + square
        print(printed_row)

def place_item(space, x, y, item):
    space[y][x] = item

# classes 
class intersection():
    def __init__(self, space, x, y, id):
        self.space = space
        self.x = x
        self.y = y
        self.id = id
        self.centerx = x + 2
        self.centery = y + 2
    
    def place(self):
        for i in range(0, 5):
            place_item(self.space, self.x+i, self.y, "#")
            place_item(self.space, self.x+i, self.y+4, "#")
        for i in range(1, 4):
            place_item(self.space, self.x, self.y+i, "#")
            place_item(self.space, self.x+4, self.y+i, "#")
        place_item(self.space, self.centerx, self.centery, self.id)

class road():
    def __init__(self, id1, id2, r_len, h_len, v_len):
        self.id = id1 + id2
        # total_length = road_length + horiztonal + vertical lengths
        self.length = r_len + h_len + v_len - 1

    def report(self):
        print(f"road ID: {self.id}\nroad length: {self.length}")

class car():
    def __init__(self, place, direction, car_id):
        self.place = place
        self.direction = direction
        self.car_id = car_id

    def report(self):
        print(f"place: {self.place}, direction: {self.direction}, id: {self.car_id}")

# functions using classes
def connect_intersections(space, intersection1, intersection2):
    cross_point = (intersection1.centerx, intersection2.centery)
    road_length = 0
    vertical_length = 0
    horizontal_length = 0
    if (intersection1.centerx == intersection2.centerx):
        # vertical line
        road_length = abs(intersection1.centery-intersection2.centery)-5
        for i in range(road_length):
            if intersection1.y < intersection2.y:
                place_item(space, intersection1.centerx, intersection1.centery+3+i, "r")
            else:
                place_item(space, intersection1.centerx, intersection1.centery-3-i, "r")
    elif (intersection1.centery == intersection2.centery):
        # horizontal line
        road_length = abs(intersection1.centerx-intersection2.centerx)-5
        for i in range(road_length):
            if intersection1.x < intersection2.x:
                place_item(space, intersection1.centerx+3+i, intersection1.centery, "r")
            else:
                place_item(space, intersection1.centerx-3-i, intersection1.centery, "r")
    else:
        directionx = 0
        directiony = 0
        # need to move in the X and Y directions using the cross_point
        if intersection1.centerx == cross_point[0]:
            # cross_point is above/below intersection1
            horizontal_length = abs(intersection2.centerx-cross_point[0])-2
        elif intersection2.centerx == cross_point[0]:
            # cross_point is above/below intersection2
            horizontal_length = abs(intersection1.centerx-cross_point[0])-2
        if intersection1.centery == cross_point[1]:
            # cross_point is left/right intersection1
            vertical_length = abs(intersection2.centery-cross_point[1])-2
        elif intersection2.centery == cross_point[1]:
            # cross_point is left/right intersection2
            vertical_length = abs(intersection1.centery-cross_point[1])-2
        if intersection1.centery < intersection2.centery:
            directiony = -1
        elif intersection1.centery > intersection2.centery:
            directiony = 1
        if intersection1.centerx < intersection2.centerx:
            directionx = 1
        elif intersection1.centerx > intersection2.centerx:
            directionx = -1
        for i in range(vertical_length):
            place_item(space, intersection1.centerx, cross_point[1]+directiony*i, "r")
        for i in range(horizontal_length):
            place_item(space, cross_point[0]+directionx*i, intersection2.centery, "r")
    return road(intersection1.id, intersection2.id, road_length, horizontal_length, vertical_length)
    

mySpace = create_array(25, 25, " ")
intersectionA = intersection(mySpace, 0, 0, "a")
intersectionB = intersection(mySpace, 7, 18, "b")
intersectionC = intersection(mySpace, 20, 0, "c")
intersectionD = intersection(mySpace, 11, 10, "d")
intersectionA.place()
intersectionB.place()
intersectionC.place()
intersectionD.place()
roadAB = connect_intersections(mySpace, intersectionA, intersectionB)
roadAC = connect_intersections(mySpace, intersectionA, intersectionC)
roadCB = connect_intersections(mySpace, intersectionC, intersectionB)
roadAD = connect_intersections(mySpace, intersectionA, intersectionD)
roadBD = connect_intersections(mySpace, intersectionB, intersectionD)

carA = car(intersectionA, "South", "a")

os.system('cls')
print_space(mySpace)
carA.report()