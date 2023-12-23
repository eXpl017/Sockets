### HTTP Server
---
  - once the server receives a req, it creates a res and sends it back
  - this http res typically consists of:
	- res status line
	- res headers (optional)
	- blank line (to mark the end of headers and the beginning of body)
	- res body (optional)
  - eg. of above:
	```
	HTTP/1.1 200 OK            # Response status 
	Server: Tornado/4.3        # Response header
	Date: Wed, 18 Oct 2017     # Response header
	Content-type: text/html    # Response header
	Content-Length: 13         # Response header
	                           # Blank line
	Hello, world!              # Response body
	```
  - status and headers are for browser/user-agent (not for display), body is for display
  - headers contain info about site/curr page
  - an http req consists of:
	- req line
	- req headers (optional)
	- blank line / separator
	- req body (optional)
  - eg. of above:
	```
	GET /index.html HTTP/1.1	# req line
	Host: www.example.com		# req header
	Connection: keep-alive		# req header
	User-Agent: Mozilla/5.0		# req header
	```
  - req line has 4 parts:
	<Method> <URI> <HTTP version> <\r\n>
	- Method tells what client wants to do on the resourse
	- URI tells where the resource is
	- HTTP version the client supports or wants the server to respond in
	- \r\n is end of req line

