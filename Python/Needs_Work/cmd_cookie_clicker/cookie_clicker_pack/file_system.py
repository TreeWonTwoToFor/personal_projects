import json

def file_update(cookies, building_list):
	global json_value
	json_value = {"cookies": cookies}
	for building in building_list:
		json_value.update({building.name: 
   		{
			"count": building.count,
			"cps": building.cps
		}})

def file_read(file_name):
	with open(file_name) as f:
		data = json.load(f)
	return data

def data_dump():
	save_file = open("save_data", "w")
	json.dump(json_value, save_file, indent = 4)
	save_file.close()

def init():
	print("file_system loaded")