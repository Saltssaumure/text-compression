# LZW compression

import math
import os

def make_codeword(integer, length):
    return bin(integer).lstrip("0b")

def read_file(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    in_file = open(path, "r")
    content = "".join(in_file.readlines())
    in_file.close()
    return content

def write_file(filename, content):
    path = os.path.join(os.path.dirname(__file__), filename)
    out_file = open(path, "w")
    out_file.write(content)
    out_file.close()

def dict_init(text):
    unique_chars = set(text)
    codeword_len = math.ceil(math.log(len(unique_chars), 2))
    dictionary = {char : make_codeword(i, codeword_len) for i, char in enumerate(unique_chars)}
    return codeword_len, dictionary

def find_long_substring(text, dictionary, text_pos):
    cur_str = text[text_pos]
    for i in range(text_pos + 1, len(text)):
        next_str = cur_str + text[i]
        if next_str not in dictionary:
            return cur_str
        else:
            cur_str = next_str
    return cur_str
                
text = read_file(input("File to encode: "))

codeword_len, dictionary = dict_init(text)

# Testing only hardcoded stuff
# text = "GACGATACGATACG"
# codeword_len = 2
# dictionary = {
#     'A' : '00',
#     'C' : '01',
#     'G' : '10',
#     'T' : '11'
# }

original_size = codeword_len * len(text)
text_pos = 0
encoded = ""

while text_pos < len(text) - 1:

    # Identify longest substring starting at text_pos
    long_substring = find_long_substring(text, dictionary, text_pos)

    # Output codeword for substring
    encoded += dictionary[long_substring].zfill(codeword_len)

    # Move to next position in text
    text_pos += len(long_substring)
    if text_pos >= len(text):
        break

    # Add new entry to dictionary
    next_char = text[text_pos]
    if len(dictionary) >= 2**codeword_len:
        codeword_len += 1
    dictionary[long_substring + next_char] = make_codeword(len(dictionary), codeword_len)

# print(text)
# print(encoded)
# print(dictionary)

write_file("compressed.txt", encoded)

encoded_size = len(encoded)

print(f"""
Original size: {original_size}
Encoded size: {encoded_size}
Size reduction: {(1 - encoded_size/original_size) * 100:.2f}%

See compressed file at compressed.txt
""")