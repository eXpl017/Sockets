# this is the client which will send req and get res from the echo server

import socket
import signal

# creating a class for the client
class TCPclient():
	# init method to initialize the server addr, default values given
	def __init__(self, host='127.0.0.1', port=10001):
		self.server_addr = (host, port)

	# method to send request to server and get response
	def client_start(self):
		self.signal_handler()

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
				data_recv = s.recv(1024)
				print(f'Data echo:\n{data_recv.decode()}')
				received += len(data_recv)
				
			print(f'All data received')

		finally:
			s.close()

	# method for handling SIGINT
	def signal_handler(self):
		print('Press Ctrl+c to stop the server.')

		# callable function for stopping the server with Ctrl+c
		def stop_client(signal, frame):
			print('\nDetected KeyboardInterrupt.')
			print('Stopping the client now...')
			raise SystemExit

		# creating a signal handler
		signal.signal(signal.SIGINT, stop_client)


if __name__ == '__main__':
	client = TCPclient()
	client.client_start()
