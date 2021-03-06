import serial, sys, time, os

def bitswap(b):
	b = (b&0xF0) >> 4 | (b&0x0F) << 4
	b = (b&0xCC) >> 2 | (b&0x33) << 2
	b = (b&0xAA) >> 1 | (b&0x55) << 1
	return b

	
# connect to device
ser = serial.Serial('COM5', 2000000, timeout=0.1)

# send "ping" command to make sure device is there
ser.write(b'\xFF')
data = ser.read()
if data == b'\xFF':
	print("+++ Connected to device, device is ready to receive commands...")
else:
	print("!!! Device is not ready, exiting...")
	sys.exit()

# open file
f = sys.stdin.buffer #open(sys.argv[1], "rb")

# stop previous
print("--- Sending stop command to device")
ser.write(b'\x00')
time.sleep(0.1)

# set window size
#ser.write(bytes([0xF0, 0x7F, 0xFF]))# 32768 = ~5.5ms

# set window off at
#ser.write(bytes([0xFC, 0x08, 0x4A])) # 2122

# start run
print("--- Sending start command to device")
ser.write(b'\x01\x02\x02\x02\x00\x00') # command 1 (play), 16-bits, 2 port, 1 dataline, sync, no window1, no window2

latches = 0
extra = 0
skip = 0


for n in range(0, skip):
	f.read(2)

cmd = None
data = None
inputs = None	
tmp = None

print("--- Starting read loop")
while True:
	cmd = ser.read()
	if cmd == b'\x0F':
		inputs = f.read(56)
		packed_pcm = inputs
		data = []

		for i in range(0, len(packed_pcm), 8):
			val = (packed_pcm[i+1] << 8) + (packed_pcm[i])
			val = val ^ 0xA804

			d1 =  (((val>>6))&1)
			d1 += (((val>>4)&1)<<1)
			d1 += (((val>>2)&1)<<2)
			d1 += (((val)&1)<<3)

			d2 = ((val>>7)&1)
			d2 += (((val>>5)&1)<<1)
			d2 += (((val>>3)&1)<<2)
			d2 += (((val>>1)&1)<<3)

			d3 = (((val>>14))&1)
			d3 += ((((val>>12))&1)<<1)
			d3 += (((val>>10)&1)<<2)
			d3 += ((((val>>8))&1)<<3)

			d4 = (((val>>15))&1)
			d4 += ((((val>>13))&1)<<1)
			d4 += ((((val>>11))&1)<<2)
			d4 += (((val>>9)&1)<<3)

			val = (packed_pcm[i+3] << 8) + (packed_pcm[i+2])
			val = val ^ 0xA804
			#val = val ^ 0xAC00

			d5 =  (((val>>6))&1)
			d5 += (((val>>4)&1)<<1)
			d5 += (((val>>2)&1)<<2)
			d5 += (((val)&1)<<3)

			d6 = ((val>>7)&1)
			d6 += (((val>>5)&1)<<1)
			d6 += (((val>>3)&1)<<2)
			d6 += (((val>>1)&1)<<3)

			d7 = (((val>>14))&1)
			d7 += ((((val>>12))&1)<<1)
			d7 += (((val>>10)&1)<<2)
			d7 += ((((val>>8))&1)<<3)

			d8 = (((val>>15))&1)
			d8 += ((((val>>13))&1)<<1)
			d8 += ((((val>>11))&1)<<2)
			d8 += (((val>>9)&1)<<3)

			val = (packed_pcm[i+5] << 8) + (packed_pcm[i+4])
			val = val ^ 0xA804

			d11 =  (((val>>6))&1)
			d11 += (((val>>4)&1)<<1)
			d11 += (((val>>2)&1)<<2)
			d11 += (((val)&1)<<3)

			d21 = ((val>>7)&1)
			d21 += (((val>>5)&1)<<1)
			d21 += (((val>>3)&1)<<2)
			d21 += (((val>>1)&1)<<3)

			d31 = (((val>>14))&1)
			d31 += ((((val>>12))&1)<<1)
			d31 += (((val>>10)&1)<<2)
			d31 += ((((val>>8))&1)<<3)

			d41 = (((val>>15))&1)
			d41 += ((((val>>13))&1)<<1)
			d41 += ((((val>>11))&1)<<2)
			d41 += (((val>>9)&1)<<3)

			val = (packed_pcm[i+7] << 8) + (packed_pcm[i+6])
			val = val ^ 0xA804
			#val = val ^ 0xAC00

			d51 =  (((val>>6))&1)
			d51 += (((val>>4)&1)<<1)
			d51 += (((val>>2)&1)<<2)
			d51 += (((val)&1)<<3)

			d61 = ((val>>7)&1)
			d61 += (((val>>5)&1)<<1)
			d61 += (((val>>3)&1)<<2)
			d61 += (((val>>1)&1)<<3)

			d71 = (((val>>14))&1)
			d71 += ((((val>>12))&1)<<1)
			d71 += (((val>>10)&1)<<2)
			d71 += ((((val>>8))&1)<<3)

			d81 = (((val>>15))&1)
			d81 += ((((val>>13))&1)<<1)
			d81 += ((((val>>11))&1)<<2)
			d81 += (((val>>9)&1)<<3)
			
			
			data = data + [bitswap(d1) + (bitswap(d5)>>4), bitswap(d11) + (bitswap(d51)>>4), bitswap(d2) + (bitswap(d6)>>4), bitswap(d21) + (bitswap(d61)>>4), bitswap(d3) + (bitswap(d7)>>4), bitswap(d31) + (bitswap(d71)>>4), bitswap(d4) + (bitswap(d8)>>4), bitswap(d41) + (bitswap(d81)>>4)]
		
		ser.write(bytes([0x0F] + data))
		latches = latches + 7
		if latches % 1200 == 0:
			print('*** Latches: [%d] - Data: [%x]' % (latches, data[0]))
