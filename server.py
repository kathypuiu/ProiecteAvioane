import random
import os
import socket
from functions import recvall
import logging
import time

logging.basicConfig(level=logging.DEBUG)

os.chdir('./boards')
def choose_file():
	"""
	Returneaza o matrice bazata pe un fisier cu o configuratie ales random.
	"""
	file_count = int(next(os.walk("."))[2][-1])
	choice = random.randint(1, file_count)
	matrice = []

	with open(str(choice), 'r') as f:
		for line in f:
			row = list(line)
			try:
				del row[10]
			except:
				pass
			matrice.append(row)

	#print(matrice)
	return matrice


def check_hit(matrice, x, y):
	"""
	Verifica daca a fost lovit un avion.
	Returneaza 0 data nu, 1 daca a fost lovit in corp, 2 daca a fost lovit in cap.
	"""
	hit = 0
	if matrice[x][y] in ('1','2','3'):
		hit = 1
	if matrice[x][y] in ('A', 'B', 'C'):
		hit = matrice[x][y]

	return hit

def server():
	NO_CLIENTS = 2
	ADDRESS = '127.0.0.1'
	PORT = 1025
	clients = []
	users = []
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((ADDRESS, PORT))
	sock.listen(NO_CLIENTS)
	print('Listening at', sock.getsockname())
	while True:
		sc, sockname = sock.accept()
		print('We have accepted a connection from', sockname)
		print(' Socket name:', sc.getsockname())
		print(' Socket peer:', sc.getpeername())
		username = recvall(sc)
		logging.debug(username)
		if username not in users:
			clients.append(sc)
			users.append(username)
			sc.sendall(b'You in.\0')
		else:
			sc.sendall(b'Nume deja luat.\0')
			sc.close()
		if len(clients) == NO_CLIENTS:
			break

	#print(clients)

	while True:
		quit = 0
		board = choose_file()
		planes = {user: {'A': 1, 'B': 1, 'C': 1} for user in users}

		while quit == 0:
			for sock in clients:
				time.sleep(0.01)
				sock.sendall(b'A\0')
				response = recvall(sock)
				user = users[clients.index(sc)]

				logging.debug(user)
				logging.debug(response)
				x, y = response.split()
				x, y = int(x), int(y)

				hit = check_hit(board, x, y)
				if hit in ('A', 'B', 'C'):
					planes[user][hit] = 0
					sock.sendall(b'X\0')
					all = 1

					for i in ('A', 'B', 'C'):
						if planes[user][i] == 1:
							all = 0
					logging.debug(planes)
					logging.debug(all)
					if all:
						for s in clients:
							s.sendall(user.encode('utf-8') + b'\0')
						logging.debug("BREAK")
						quit = 1
						break

				if hit == 1:
					sock.sendall(b'1\0')

				if hit == 0:
					sock.sendall(b'0\0')





if __name__ == "__main__":
	server()