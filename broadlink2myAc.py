import broadlink2lirc as b2c
import os

class acPkt(b2c.broadPkt):
	ONE = (53,15)
	ZERO = (15,53)
	MODE = {69: 'cool', 66: 'heat', 19: 'vent', 20: 'hum'}
	def __init__(self, temp, mode, fan):
		self.temp = temp
		self.mode = mode
		self.fan = fan
		print "temp {} mode {}".format(self.temp, self.MODE[self.mode])

	@classmethod
	def decode(cls, lirc_pkt):
		lirc_norm = []
		for i in lirc_pkt:
	                if i > (60):
                        	lirc_norm.append(i)
                	elif i > (25):
                        	lirc_norm.append(53)
                	else:
                        	lirc_norm.append(15)
		iter_lirc_norm = iter(lirc_norm)
		ir_data = ""
        	for tup in zip(iter_lirc_norm, iter_lirc_norm):
                	if (tup == acPkt.ONE):
                        	ir_data = ir_data + '1'
                	elif (tup == acPkt.ZERO):
                        	ir_data = ir_data + '0'
                	else:
                        	ir_data = ir_data + 'x'

		temp = int(ir_data[26:17:-1], 2)
		mode = int(ir_data[16:8:-1], 2)
		return cls(temp, mode, 0)

def main():
	path ="ac_samples"
	for filename in os.listdir(path):
		abs_filename = os.path.join(path, filename)
		print filename
		fd = open(abs_filename)
		data_base64 = fd.read()
		bp = b2c.broadPkt.fromBase64(data_base64)
		ac_pkt = acPkt.decode(bp)
		fd.close()

if __name__== "__main__":
	main()
