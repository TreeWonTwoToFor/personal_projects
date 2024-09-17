import os
import time
from cookie_clicker_pack import file_system

upgrade_price = 100
cookies = 0
click_power = 1
current_cps = 0.0
os.system('cls')

class building:
	def __init__(self, count, cps, base_cost, name):
		self.count = count
		self.cps = cps
		self.base_cost = base_cost
		self.name = name
	
	def self_report(self):
		print(f'building: {self.name} \ncount: {self.count}\ncps: {self.cps}\nbase_cost: {self.base_cost}\ncurrent cost: {self.cost_calculate()}')

	def cost_calculate(self):
		cost = self.base_cost * 1.15**(self.count)
		return cost
	
	def buy_building(self):
		global cookies
		if cookies >= self.cost_calculate():
			cookies -= self.cost_calculate()
			self.count += 1
			terminal.display()
	
	def click(self):
		global cookies
		cookies += (self.cps * self.count)

cursor = building(0, 0.1, 15, 'cursor')
grandma = building(0, 1, 100, 'grandma')
farm = building(0, 8, 1100, 'farm')
mine = building(0, 47, 12000, 'mine')
building_list 		= [cursor, grandma, farm, mine]
building_name_list 	= []
for buildings in building_list:
	building_name_list.append(buildings.name)
	
class terminal:
	def display():
		os.system('cls')
		print(f"Cookies: {int(cookies)}, CPS: {current_cps}, Upgrade: {upgrade_price}\n--------------------------")
		for building in building_list:
			print(f'{building.name}: {building.count}\n\t{int(building.cost_calculate())}')
		print('\n')

	def read_text(text):
		text_list = text.split()
		text_list_length = len(text_list)
		if len(text_list) != 0:
			if text_list[0] == "exit":
				global running
				running = False
			elif text_list[0] == "ls":
				print("exit, ls, report, click, cookies, display, buy")
			elif text_list[0] == "report":
				if text_list_length == 1:
					for buildings in building_list:
						print(buildings.name)
				elif text_list[1] == "list":
					for buildings in building_list:
						print(buildings.name)
				elif text_list[1] in building_name_list:
					for j in range(0, len(building_name_list)):
						if text_list[1] == building_name_list[j]:
							building_list[j].self_report()
				else:
					print("ERROR: non-existant command")
			elif text_list[0] == "click" or text_list[0] == "c":
				global cookies
				global click_power
				cookies += click_power
				terminal.display()
			elif text_list[0] == "cookies":
				return cookies
			elif text_list[0] == "buy":
				if text_list_length == 1:
					print("please list the building name")
				elif text_list[1] in building_name_list:
					for j in range(0, len(building_name_list)):
						if text_list[1] == building_name_list[j]:
							building_list[j].buy_building()
				elif text_list[1] == "upgrade":
					global upgrade_price
					if cookies >= upgrade_price:
						cookies -= upgrade_price
						click_power = click_power * 2
						upgrade_price = upgrade_price * 2
					terminal.display()
			elif text_list[0] == "display":
				terminal.display()
			elif text_list[0] == "cps":
				global current_cps
				current_cps = 0
				for building in building_list:
					current_cps += (building.cps * building.count)
				return current_cps
			elif text_list[0] == "password":
				click_power = 10000

def run_game():
	current_time = time.time()
	terminal.display()
	running = True
	while running:
		text_input = input("Cookie Clicker> ")
		if (time.time()- current_time) > 1:
			amount_to_count = int(time.time()- current_time)
			current_time = time.time()
			for i in range(0, amount_to_count):
				for building in building_list:
					building.click()
			current_cps = 0
			for building in building_list:
				current_cps += (building.cps * building.count)
		terminal.read_text(text_input)	
	file_system.file_update(cookies, building_list)
	file_system.data_dump()