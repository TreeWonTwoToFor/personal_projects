import os

def print_screen(car_position, timer):
    os.system("cls")
    a = "   "
    b = "   "
    c = "   "
    roadSegAB = "           "
    roadSegBC = [" ", " ", " ", " ", " "]
    if car_position == "intersectionA":
        a = " c "
    elif car_position == "intersectionB":
        b = " c "
    elif car_position == "intersectionC":
        c = " c "
    elif car_position == "roadAB":
        roadSegAB = ""
        tenth_second = int((timer-1)*10)
        for i in range(0, tenth_second):
            roadSegAB = roadSegAB + " "
        roadSegAB = roadSegAB + "c"
        for i in range(0, 10-tenth_second):
            roadSegAB = roadSegAB + " "
    elif car_position == "roadBC":
        roadSegBC = []
        tenth_second = int((timer-3)*10)
        fifth_second = 0
        if tenth_second % 2 == 0:
            fifth_second = tenth_second/2
        else:
            fifth_second = (tenth_second-1)/2
        for i in range(0, int(fifth_second)):
            roadSegBC.append(" ")
        roadSegBC.append("c")
        for i in range(0, 5-int(fifth_second)):
            roadSegBC.append(" ")
    print(f"#####           #####")
    print(f"#   #           #   #")
    print(f"#{a}#-----------#{b}#")
    print(f"#   #{roadSegAB}#   #")
    print(f"#####           #####")
    print(f"                 {roadSegBC[0]}|  ")
    print(f"                 {roadSegBC[1]}|  ")
    print(f"                 {roadSegBC[2]}|  ")
    print(f"                 {roadSegBC[3]}|  ")
    print(f"                 {roadSegBC[4]}|  ")
    print(f"                #####")
    print(f"                #   #")
    print(f"                #{c}#")
    print(f"                #   #")
    print(f"                #####")