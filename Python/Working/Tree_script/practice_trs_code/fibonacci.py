import time
start_time = time.time()
value1 = 0
value2 = 1
amount = 100
out_list = []

for i in range(0, amount):
    sum_value = value1 + value2
    value1 = value2
    value2 = sum_value
    out_list.append(sum_value)

print(out_list)

end_time = time.time() - start_time
print(end_time)