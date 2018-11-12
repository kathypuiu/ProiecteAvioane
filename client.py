from functions import recvall
import socket
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

def print_board(board):
	print("  0 1 2 3 4 5 6 7 8 9")
	for row in range(10):
		print("{} ".format(row), end='')
		for col in range(10):
			if board[row][col] == '0':
				print(". ", end='')
			elif board[row][col] == '1':
				print("* ", end='')
			else:
				print("X ", end='')
		print('')

def client():
	ADDRESS = '127.0.0.1'
	PORT = 1025
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ADDRESS, PORT))
	logging.debug('Client has been assigned socket name' + str(sock.getsockname()))
	username = sys.argv[1]
	username = username.encode('utf-8') + b'\0'
	sock.sendall(username)
	response = recvall(sock)
	print(response)

	while True:
		board = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
				['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]


		print("Incepe jocul!")
		print_board(board)
		while True:
			response = recvall(sock)
			logging.debug("A="+response + " " + str(response == 'A'))
			logging.debug(str(len(response)) + " " + str(len('A')))
			if response == 'A':
				print("Alege coordonatele: ")
			else:
				print("Userul " + response + " a distrus toate avioanele.")
				break
			x = ''
			y = ''
			ok = 0
			while ok == 0:
				x = input("Introdu coordonata X (0-9): ")
				y = input("Introdu coordonata y (0-9): ")
				try:
					if int(x) not in range(10) or int(y) not in range(10):
						print("you mofo")
						continue
				except ValueError:
					print("you mofo")
					continue
				ok = 1

			coo = x + ' ' + y
			sock.sendall(coo.encode('utf-8') + b'\0')
			x, y = int(x), int(y)
			response = recvall(sock)
			if response == 'X':
				print("Ai distrus un avion.")
				board[x][y] = 'X'
				print_board(board)
			if response == '1':
				print("Ai lovit un avion.")
				board[x][y] = '1'
				print_board(board)
			if response == '0':
				print("Nu ai lovit nimic.")
				print_board(board)






if __name__ == "__main__":
	client()