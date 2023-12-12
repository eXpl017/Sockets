# implementation of HTTP server by changing code in the echo server directly

import socket
import signal

# creating a class for the server
class TCPserver():
	# init method to define the host and port, default values given
	def __init__(self, host='127.0.0.1', port=10001):
		self.host = host
		self.port = port

	# method to start the server
	def start(self):
		print('Starting the server now...')

		self.signal_handler()

		# creating socket obj, server is TCP based, using ipv4
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			# binding the socket to host ip and port
			s.bind((self.host, self.port))
		except socket.error as msg:
			# print(f'Bind Error: {str(msg[0])} - {msg[1]}')
			raise SystemExit

		# listen(n) means that we will queue up for connec to be made before denying any further req
		s.listen(5)

		print(f'Listening on {s.getsockname()}')

		# keep listening for connections
		while True:
			conn, client_addr = s.accept()

			try:
				print(f'Connected by Client {client_addr}')

				while True:
					# recv(n) means that we will read only first n bytes of data, and with while loop we can keep reading till the end
					data_recv = conn.recv(1024)

					to_send = self.handle_request(data_recv)

					if not to_send:
						break
					else:
						conn.sendall(to_send)

			finally:
				conn.close()

	# process the received data and send
	def handle_request(self, data_recv):
		# if there is data, send it as it is back to the client
		if data_recv:
			print(f'Data received: {data_recv}')
			return data_recv
		else:
			print(f'No data received')
			return 0

	# method for handling SIGINT
	def signal_handler(self):
		print('Press Ctrl+c to stop the server.')

		# callable function for stopping the server with Ctrl+c
		def stop_server(signal, frame):
			print('\nDetected KeyboardInterrupt.')
			print('Stopping the server now...')
			raise SystemExit

		# creating a signal handler
		signal.signal(signal.SIGINT, stop_server)


class HTTPserver(TCPserver):
	def handle_request(self, data_recv):
		if data_recv:
			res_status = b"HTTP/1.1 200 OK\r\n"
			blank = b'\r\n'
			res_body = b'Received data!'
			return b''.join([res_status, blank, res_body])
		else:
			return 0

if __name__ == '__main__':
	server = HTTPserver()
	server.start()
