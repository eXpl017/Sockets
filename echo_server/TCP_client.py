# this is the client which will send req and get res from the echo server

import socket

# creating a class for the client
class TCPclient():
	server_addr = ('127.0.0.1',10001)

	# method to send request to server and get response
	def client_start(self):
		# creating socket obj, TCP based using IPv4
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# connecting to server		
		try:
			print(f'Connecting to server at {self.server_addr}')
			s.connect(self.server_addr)
		except:
			print(f'an error occuring here!')
			raise SystemExit

		try:
			# sending message to server in bytes
			message = b'This is a message.\nIt will be repeated.'
			s.sendall(message)

			# checking for response from server
			received = 0
			expected = len(message)

			while received < expected:
				data_recv = s.recv(16)
				print(f'Data echo: {data_recv}')
				received += len(data_recv)
				
			print(f'All data received')

		finally:
			s.close()

if __name__ == '__main__':
	client = TCPclient()
	client.client_start()
