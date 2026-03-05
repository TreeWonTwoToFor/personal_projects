from trc_pack import interperter

new_stack = interperter.Stack()

print(new_stack)
new_stack.push("hello")
print(new_stack)
new_stack.push("world")
print(new_stack)
print(new_stack.size())
value = new_stack.pop()
print(value)
print(new_stack)
