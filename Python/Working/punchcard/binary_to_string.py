import os

os.system('cls')

def binary_to_string(bits):
    return ''.join([chr(int(i, 2)) for i in bits])

def splice_binary(text):
    output_list = []
    byte_count = len(text) / 8
    for i in range(0, int(byte_count)):
        j = i*8
        output_list.append(text[j:j+8])
    return output_list


binary_text = input("binary> ")
s = binary_to_string(splice_binary(binary_text))
print(s)