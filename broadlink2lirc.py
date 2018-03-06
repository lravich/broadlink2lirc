import binascii
import struct
import os


class lircPkt:
	def __iter__(self):
		return iter(self.lirc_pkt)
		
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
	def __init__(self, pulse_list):
		self.lirc_pkt = pulse_list

class broadPkt(lircPkt):
	IR_CODE = 0x26
	IR="IR"
	RF="RF"
	def __str__(self):
		return "Type: {} Repeat: {} length {} \n {}".format(self.type, self.repeat, self.len, lircPkt.__str__(self))

	def __init__(self, pkt_type, repeat, length, pulse_list):
		self.type = pkt_type
		self.repeat = repeat
		self.len = length
		lircPkt.__init__(self, pulse_list)
	
	@classmethod
	def fromBase64(cls, data):
		bytes_raw = bytearray(data.decode("base64"))
		if (int(bytes_raw[0]) == broadPkt.IR_CODE):
			pkt_type = broadPkt.IR
		else:
			pkt_type = broadPkt.RF

		repeat = int(bytes_raw[1])
		length = struct.unpack("<H", bytes_raw[2:4])[0]
		if (pkt_type == broadPkt.IR):
			lirc_data = bytes_raw[4:]
			pulse_list = []
			i = 0
			while(1):
				if (int(lirc_data[i]) == 0):
					pulse_list.append(struct.unpack(">H", lirc_data[i+1:i+3])[0])
					i = i + 3
				else:
					pulse_list.append(int(lirc_data[i]))
					i = i + 1
				if (i == length):
					break
			return cls(pkt_type, repeat, length, pulse_list)
		else:
			raise NotImplemented
			
def example():
	path ="ac_samples"
	for filename in os.listdir(path):
		abs_filename = os.path.join(path, filename)
		fd = open(abs_filename)
		data_base64 = fd.read()
		bp = broadPkt.fromBase64(data_base64)
		print bp
		fd.close()

if __name__== "__main__":
	example()
