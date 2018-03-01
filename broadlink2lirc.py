import binascii
import struct
import os
class lircPkt:
	def __str__(self):
		out = ""
		i = 0
		for pulse in self.lirc_pkt:
			out = out + str(pulse) + " "
			i = i + 1
			if (i % 16 == 0):
				out = out + "\n"
		return out
	
		return self.lirc_pkt.__str__()
	def __init__(self, data, length):
		self.lirc_pkt = []
		i = 0
		while(1):
			if (int(data[i]) == 0):
				self.lirc_pkt.append(struct.unpack(">H", data[i+1:i+3])[0])
				i = i + 3
			else:
				self.lirc_pkt.append(int(data[i]))
				i = i + 1
			if (i == length):
				break
class broadPkt:
	def __str__(self):
		return "Type: {} Repeat: {} length {} \n {}".format(self.type, self.repeat, self.len, self.lirc)
	def decode_ir(self, ir_data):
		self.lirc = lircPkt(ir_data, self.len)
	def decode(self, data):
		bytes_raw = bytearray(data.decode("base64"))
		if (int(bytes_raw[0]) == 0x26):
			self.type = "IR"
		else:
			self.type = "RF"
		self.repeat = int(bytes_raw[1])
		self.len = struct.unpack("<H", bytes_raw[2:4])[0]
		if (self.type == "IR"):
			self.decode_ir(bytes_raw[4:])

	def __init__(self, data):
		if (data):
			self.decode(data)

		
def main():
	path ="/home/leonid/ac_samples"
	out_file = open("ac_dec",'w')
	for filename in os.listdir(path):
		abs_filename = os.path.join(path, filename)
		fd = open(abs_filename)
		data_base64 = fd.read()
		bp = broadPkt(data_base64)
		print bp
		fd.close()
	#	out_file.write(filename + "->" + dec_data + "\n")

	out_file.close()

if __name__== "__main__":
	main()
