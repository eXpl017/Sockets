# implementation of HTTP server by changing code in the echo server directly

import socket
import signal
from copy import deepcopy

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
	# init method for this class. in python if you create init of inherited class, it overrides the init of parent class. so to have this init do init of parent class and have its own functions, call the parents class init by using super()
	def __init__(self, host='127.0.0.1', port=10001):
		super().__init__(host, port)
		self.status_codes = {
			200:'OK',
			404:'Not Found'
		}
		self.headers = {
			'Server': 'Lmao Server',
			'Content-type': 'text/html'
		}

	# overriding the handle_request method from parent class
	def handle_request(self, data_recv):
		if data_recv:
			res_status = self.res_status(200)
			res_headers = self.res_headers()
			blank = '\r\n'.encode()
			res_body = """<html><body><h1>This is the LMAO server!</body></html>""".encode()
			return b''.join([res_status, res_headers, blank, res_body])
		else:
			return 0

	# method to return the response status line when called with the status code
	def res_status(self, status_code):
		return f'HTTP/1.1 {status_code} {self.status_codes[status_code]}\r\n'.encode()

	# method to return response headers, can add extra headers by passing extra_headers dict when calling
	def res_headers(self, extra_headers=None):
		# creates deep copy of the headers dict
		headers_copy = deepcopy(self.headers)

		if extra_headers:
			headers_copy = headers_copy.update(extra_headers)

		headers = ""

		for header in headers_copy:
			headers += f"{header}: {headers_copy[header]}\r\n"

		return headers.encode()

if __name__ == '__main__':
	server = HTTPserver()
	server.start()
