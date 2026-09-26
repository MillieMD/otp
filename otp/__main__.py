# IMPORTS
import sys
import os
import argparse

#FILE LOCATIONS
CONFIG_FOLDER = os.getenv("HOME") + "/.config/otp/"
CODE_BOOK_FILE = "codebook.txt"
CONVERSION_TABLE_FILE = "conversiontable.txt"

# INDICATORS
CODE_INDICATOR = "0"
FIG_INDICATOR = "90"

# DICTIONARY FUNCTIONS
def init_dict(filename) -> dict:
    """Initialise a dictionary by reading from a file. 
    Assumes comma seperated key value pairs, one per line."""

    d = {}

    with open(filename) as file:
        for line in file:
            key, value = line.split(",")
            d[key.strip()] = value.strip()

    return d


def key_from_dict_value(d, value) -> list:
    """Retrieve keys from a dictionary based on their value"""

    return [key for key, item in d.items() if item == value]


# VALIDATE CONFIG
def is_valid_config(file_path : str) -> bool:
    """Ensure that config files are using the expected format"""

    with open(file_path) as file:
        for line in file:
            if not is_valid_config_line(line): return False

    return True


def is_valid_config_line(line) -> bool:
    """Check that config lines are in expected format.
    Valid format: [int],[str]"""

    split = line.split(",")

    if len(split) != 2:
        return False

    if not split[0].strip().isdigit():
        return False

    return True


# ENCODING
def encode_as_digits(code_book : dict, conversion_table : dict, message : str) -> str:

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
                    if not prev_c.isdigit():
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
        n = int(grid[i])
        c = int(c)

        if c < n:
            c += 10
        
        cipher += str((c - n))

        i += 1

    cipher = key + cipher

    return cipher
         
        
# DECODING
def decode_digits(message) -> str :
    return ""


def cipher_to_digits(grid, key, digits) -> str :
    return ""


# DISPLAY FORMATTING
def print_digits(digits) -> None:
    """Print digits in groups of 5"""

    count = 0
    for c in digits:
        print(c, end = "")
        count += 1

        if count % 5 == 0:
            print(" ", end = "")


def main():
    main_parser = argparse.ArgumentParser(
        prog="otp",
        description="Encode and decode OTP messages",
    )

    main_parser.add_argument("--code-book", action="store_true", help="Print the location of the codebook.txt file")
    main_parser.add_argument("--conversion", action="store_true", help="Print the location of the conversiontable.txt file")

    subparsers = main_parser.add_subparsers(dest="subcommand", help="subcommand help")

    encode_parser = subparsers.add_parser("encode", help="Encode a message using the OTP protocol")
    encode_parser.add_argument('message', type=str, help='Message to encode')

    decode_parser = subparsers.add_parser("decode", help="Decode a message that was sent using the OTP protocol")
    decode_parser.add_argument('message', type=str, help='Message to decode')

    args = main_parser.parse_args()

    if args.code_book:
        print("The code book values are read from: ", CONFIG_FOLDER + CODE_BOOK_FILE)
        return

    if args.conversion:
        print("The conversaion table values are read from ", CONFIG_FOLDER + CONVERSION_TABLE_FILE)
        return

    if not is_valid_config(CONFIG_FOLDER + CODE_BOOK_FILE):
        print("ERROR: Invalid code book formatting", file=sys.stderr)
        exit(1)

    if not is_valid_config(CONFIG_FOLDER + CONVERSION_TABLE_FILE):
        print("Invalid conversion table formatting", file=sys.stderr)
        exit(1)

    code_book = init_dict(CONFIG_FOLDER + CODE_BOOK_FILE)
    conversion_table = init_dict(CONFIG_FOLDER + CONVERSION_TABLE_FILE)

    pad = "1234567897864913561937567328961349"
    key = pad[0:5]

    if args.subcommand == "encode":
        digits = encode_as_digits(code_book, conversion_table, args.message.upper())
        cipher = digits_to_cipher(pad, key, digits)

        print_digits(cipher)

    elif args.subcommand == "decode":
        print("TODO: decode")

