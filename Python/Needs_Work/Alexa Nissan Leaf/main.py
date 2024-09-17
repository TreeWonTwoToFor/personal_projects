import time
import os

def get_time(hour_system):
    from datetime import datetime
    now = datetime.now()  
    my_hour = now.hour
    if my_hour > 12 and hour_system == "12":
        my_hour = my_hour - 12
    return ("%s:%s:%s" % (my_hour,now.minute,now.second)) 

def get_charge_time(percent):
    percent_to_charge = 80-int(percent)
    hours_to_charge = percent_to_charge / 10
    return hours_to_charge

os.system("cls")
percent = input("put in the car's current battery> ")
current_time = (get_time("24"))
hours_left = get_charge_time(percent)
minutes_left = int((hours_left-int(hours_left))*60)
if hours_left < 0:
    print("you're all good to go!")
else:
    print("%s\n%s \n%s:%s"%(current_time, hours_left, int(hours_left), minutes_left))
