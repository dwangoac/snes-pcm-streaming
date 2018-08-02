#!/usr/bin/env python
import sys
import os
name = ""
base_name = ""

if sys.argv[1] == "":
	print("You need to specify a file to convert")
	sys.exit()
else:
	name = sys.argv[1]
	
f = open(os.path.dirname(os.path.realpath(__file__)) + "\\" + name, "rb")
fo = open(os.path.dirname(os.path.realpath(__file__)) + "\\" + name + ".r16m", "wb")
foo = open(os.path.dirname(os.path.realpath(__file__)) + "\\" + name + ".inp", "wb")

data = [int(x) for x in f.read()]

entry = (data[0]<<16) + (data[1]<<8) + (data[2])
target = entry

out = [0xC2, 0xEA, 0xCB, 0x10, 0x00, 0x00, 0x00, 0x00, 0x64, 0x30, 0xF8, 0x80, 0x00, 0x00, 0x00, 0x00]
fo.write(bytes(out))

out = [0xEA, 0xC2, 0x30, 0x64, 0x10, 0xCB, 0x80, 0xF8]
foo.write(bytes(out))


for i in range(3, len(data), 2):
	out = [data[i], 0xA9, 0xCB, 0x10, 0x00, 0x00, 0x00, 0x00, 0x64, data[i+1], 0xF8, 0x80, 0x00, 0x00, 0x00, 0x00]
	fo.write(bytes(out))

	out = [target&0xFF, 0x8D, 0xCB, 0x10, 0x00, 0x00, 0x00, 0x00, 0x64, (target>>8)&0xFF, 0xF8, 0x80, 0x00, 0x00, 0x00, 0x00]
	fo.write(bytes(out))
	
	out = [0xA9, data[i], data[i+1], 0x64, 0x10, 0xCB, 0x80, 0xF8]
	foo.write(bytes(out))

	out = [0x8D, target&0xFF, (target>>8)&0xFF, 0x64, 0x10, 0xCB, 0x80, 0xF8]
	foo.write(bytes(out))
	target += 2
	

out = [entry&0xFF, 0x5C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, (entry>>16)&0xFF, (entry>>8)&0xFF, 0xF8, 0x80, 0x00, 0x00, 0x00, 0x00]
fo.write(bytes(out))

out = [0x5C, entry&0xFF, (entry>>8)&0xFF, (entry>>16)&0xFF, 0x00, 0x00, 0x80, 0xF8]
foo.write(bytes(out))

fo.close()
foo.close()
	