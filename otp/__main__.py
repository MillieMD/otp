# IMPORTS
import sys
import time
import winsound # Look into beeps for linux so i can make this portable
import argparse

# INDICATORS
CODE_INDICATOR = "0"
FIG_INDICATOR = "90"

# MORSE CODE CONSTANTS
FREQ = 900

TIME_UNIT_MILLISECONDS = 300
DOT_MILLISECONDS = 1 * TIME_UNIT_MILLISECONDS
DASH_MILLISECONDS = 3 * TIME_UNIT_MILLISECONDS
SECONDS_BETWEEN_LETTERS = (3 * TIME_UNIT_MILLISECONDS)/1000 # convert s to milliseconds
SECONDS_BETWEEN_WORDS = (7 * TIME_UNIT_MILLISECONDS)/1000 # convert s to milliseconds

# OUTPUT
ID_REPEAT = 3

# DICTIONARY FUNCTIONS
def init_dict(d, filename) -> dict:

    f = open(filename)
    content = f.read()

    for line in content.split("\n"):
        key, value = line.split(",")
        d[key.strip()] = value.strip()
    

def key_from_dict_value(d, value):
    return [key for key, item in d.items() if item == value]


# MORSE CODE STUFF
def play_from_string(string : str):
    for c in string:
        if c == ".":
            winsound.Beep(FREQ, DOT_MILLISECONDS)

        if c == "-":
            winsound.Beep(FREQ, DASH_MILLISECONDS)

# ENCODING
def encode_as_digits(message : str) -> str:

    message_split = message.split(" ")
    digits = ""

    for word in message_split:

        if word in code_book.values():
            digits += CODE_INDICATOR
            digits += (key_from_dict_value(code_book, word))[0]

        else:

            prev_c = ""
            
            for c in word:
                if c.isdigit():
                    if prev_c.isdigit() == False:
                        digits += FIG_INDICATOR 
                    
                    digits += c*2

                else:
                    digits += (key_from_dict_value(conversion_table, c))[0]

                prev_c = c

    return digits


def digits_to_cipher(grid, key, digits) -> str:

    grid = grid.split(key)[1] # key should ONLY appear once in the whole grid
    cipher = ""

    i = 0

    for c in digits:
        n = grid[i]
        
        c_int = int(c)
        n_int = int(n)

        if c_int < n_int:
            c_int += 10
        
        cipher += str((c_int - n_int))

        i += 1

    cipher = key + cipher

    return cipher
         
        
# DECODING
def decode_digits(message) -> str :
    return ""

def cipher_to_digits(grid, key, digits) -> str :
    return ""

# DISPLAY FORMATTING
def print_digits(digits):
    count = 0
    for c in digits:
        print(c, end = "")
        count += 1

        if count % 5 == 0:
            print(" ", end = "")

# code_book = {}
# conversion_table = {}

# pad = "12345678987654321546372819978676564635241"
# key = "12345"

init_dict(code_book, "codebook.txt")
init_dict(conversion_table, "conversiontable.txt")

plaintext = sys.argv[1]
plaintext = plaintext.upper()

# digits = encode_as_digits(plaintext)
# cipher = digits_to_cipher(pad, key, digits)

# print_digits(cipher)

def main():
    main_parser = argparse.ArgumentParser(
        prog="otp",
        description="Encode and decode OTP messages",
    )

    main_parser.add_argument("--code-book", action="store_true", help="Print the location of the codebook.txt file")
    main_parser.add_argument("--conversion", action="store_true", help="Print the location of the conversiontable.txt file")

    subparsers = main_parser.add_subparsers(help="subcommand help")

    encode_parser = subparsers.add_parser("encode", help="Encode a message using the OTP protocol")
    encode_parser.add_argument('message', type=str, help='Message to encode')

    decode_parser = subparsers.add_parser("decode", help="Decode a message that was send using the OTP protocol")
    decode_parser.add_argument('message', type=str, help='Message to decode')

    args = main_parser.parse_args()

