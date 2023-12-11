# this type of server returns the same data it receives

import socket
import signal

# creating a class for the server
class TCPserver():
	host = '127.0.0.1'
	port = 10001

	# method to start the server
	def start(self):	
		print('Starting the server now...')
		print('Press Ctrl+c to stop the server.')

		# creating a signal handler
		signal.signal(signal.SIGINT, self.stop_server)

		# creating socket obj, server is TCP based, using ipv4
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			# binding the socket to host ip and port
			s.bind((self.host, self.port))
		except socket.error as msg:
			# print(f'Bind Error: {str(msg[0])} - {msg[1]}')
			raise SystemExit

		# listen(n) means that we will queue up for connec to be made before denying any further req
		s.listen(1)

		print(f'Listening on {s.getsockname()}')

		# keep listening for connections
		while True:
			conn, client_addr = s.accept()

			try:
				print(f'Connected by Client {client_addr}')

				while True:
					# recv(n) means that we will read only first n bytes of data, and with while loop we can keep reading till the end
					data_recv = conn.recv(16)
					
					# if there is data, send it as it is back to the client
					if data_recv:
						print(f'Data received: {data_recv}')
						conn.sendall(data_recv)
					else:
						print(f'No data received')
						break
			finally:
				conn.close()

	# callable function for stopping the server with Ctrl+c
	def stop_server(self, signal, frame):
		print('\nDetected KeyboardInterrupt.')
		print('Stopping the server now...')
		raise SystemExit


if __name__ == '__main__':
	server = TCPserver()
	server.start()
