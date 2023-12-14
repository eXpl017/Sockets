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
  - headers contn info about site/curr page

