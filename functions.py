import socket

def recvall(sock):
	"""
	 Citeste din socket pana simbolul de final e intalnit.
	"""
	END_DELIMITER = b'\0'
	message = b''
	while True:
		more = sock.recv(128)
		#print('Received {} bytes'.format(len(more)))
		message += more
		if END_DELIMITER in more:
			break
	message = message.decode('utf-8')
	message = message.strip()
	message = message[:-1]
	return message