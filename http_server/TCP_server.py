# implementation of HTTP server by changing code in the echo server directly

import os
import socket
import signal
from copy import deepcopy
import mimetypes

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
			404:'Not Found',
			501:'Not Implemented'
		}
		self.headers = {
			'Server': 'Lmao Server',
			'Content-type': 'text/html'
		}

	# overriding the handle_request method from parent class
	def handle_request(self, data_recv):
		if data_recv:
			# print(data_recv)
			req = HTTPrequest(data_recv)

			# getattr can be used to get the attr or method, here we use it to get the method for handling the req
			# as that method is in this class itself, we using 'self'
			try:
				handle = getattr(self, f'handle_{req.method}')		# this does run the function
			except AttributeError:
				# if we dont have the method to handle that specific req method, we send 501 res (Not Implemented)
				handle = self.HTTP_501

			return handle(req)

		else:
			return 0

	# simple response, no checking of req line etc.
	def simple_res(self, data_recv):			# changed it to check output, earlier name is simple_res
		if data_recv:
			res_status = self.res_status(200)
			res_headers = self.res_headers()
			blank = '\r\n'.encode()
			res_body = """<html><body><h1>Hello, this is LMAO server!</h1></body></html>""".encode()
			return b''.join([res_status, res_headers, blank, res_body])
		else:
			return 0

	# handle GET req
	def handle_GET(self, req):
		filename = req.uri.strip(b'/').decode()

		if filename == "":
			res_status = self.res_status(200)
			res_headers = self.res_headers()
			blank = '\r\n'.encode()
			res_body = """<html><body><h1>Hello, this is LMAO server!</h1></body></html>""".encode()
			return b''.join([res_status, res_headers, blank, res_body])

		if os.path.exists(filename):
			content_type = mimetypes.guess_type(filename)[0]
			print(content_type)
			extra_headers = {"Content-type": content_type}

			res_status = self.res_status(200)
			with open(filename,'rb') as f:
				res_body = f.read()
				# res_body = f"""<html><body><h1>Hello, this is LMAO server!</h1></body></html>""".encode()
		else:
			res_status = self.res_status(404)
			res_body = b'<h1>404 Not Found</h1>'

		blank = '\r\n'.encode()
		res_headers = self.res_headers(extra_headers)

		return (b''.join([res_status, res_headers, blank, res_body]))

	# method for telling that a method is not implmented
	# notice that the param req is not used in the function
	def HTTP_501(self, req):
		res_status = self.res_status(501)
		res_headers = self.res_headers()
		blank = '\r\n'.encode()
		res_body = "<h1>Not Implemented!</h1>".encode()
		return b''.join([res_status, res_headers, blank, res_body])

	# method to return the response status line when called with the status code
	def res_status(self, status_code):
		return f'HTTP/1.1 {status_code} {self.status_codes[status_code]}\r\n'.encode()

	# method to return response headers, can add extra headers by passing extra_headers dict when calling
	def res_headers(self, extra_headers=None):
		# creates deep copy of the headers dict
		headers_copy = deepcopy(self.headers)

		if extra_headers:
			headers_copy.update(extra_headers)

		headers = ""

		for header in headers_copy:
			headers += f"{header}: {headers_copy[header]}\r\n"

		return headers.encode()


# class defining the request, and parsing it
class HTTPrequest:
	# defining the defaults and parsing them
	def __init__(self, data):
		self.method = None
		self.uri = None
		self.http_version = '1.1'

		self.parse_req_line(data)

	# this method is just to parse the first line i.e req line
	def parse_req_line(self, data):
		lines = data.split(b'\r\n')
		req_line = lines[0]
		words = req_line.split(b' ')

		self.method = words[0].decode()

		# the below is something i was unable to confirm online. as per HTTP/1.1 standards, even if the req is for homepage, '/' has to be included for URI
		# sometimes browsers omit the URI completely when the req is to homepage of a website (not even including the '/'), so the below is to handle that
		if len(words) == 2:
			self.http_version = words[1]
		else:
			self.http_version = words[2]

		self.uri = words[1]


if __name__ == '__main__':
	server = HTTPserver()
	server.start()
