import socket
import base64
import random
from string import ascii_lowercase


s = socket.socket(socket.AF_INET, socket.SOCK_STEAM)

s.bind((127.0.0.1, 1333))

s.listen(5)

print("[+] Listerning...")

while True:
	client, address = s.accept()
	print("[+] Received connection from -> {}".format(client))

	encoded_data = clien.recv(4096)
	client.close()


	random_fd = open("".joim(random.choices(ascii_lowercase, k=10)), "w")
	random_fd.write(base64.b64decode(encoded_data).decode("utf-8"))
	random_fd.close()
