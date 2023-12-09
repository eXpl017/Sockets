> Notes made from [PYMOTW](https://pymotw.com/3/socket)

## Sockets:
  - an endpoint of a comminication channel used by prog to pass data back and forth
  - two properties controlling the way they send data:
    - address family: controls network layer protocol
    - socket type: controls transport layer protocol

Python has 3 address famimlies:
  - AF_INET: for ipv4 addressing, takes ip in the format x.x.x.x
  - AF_INET6: for ipv6 addressing
  - AF_UNIX: address family for Unix Domain Sockets (UDS), which is an IPC protocol. its implementation allows data passing directly between processes, without going through network stack. restricted to processes on the same system. is more effective than AF_INET

Socket type is usually SOCK_DGRAM for message oriented datagram transport or SOCK_STREAM for stream oriented.
Datagram sockets are usually associated with UDP, and stream sockets with TCP.
  - for reliable, in order delivery needed - TCP handles automatically
  - for delivery where order not important, small messages, or multicasting - UDP

## Functions

### Lookup Info 
  - Use ```gethostname()``` to get current systems hostname
  - Use ```gethostbyname("<hostname>")``` to get the IP of the host
  - To get more info about host, ```gethostbyname_ex("<hostname>")```. This gives us canonical hostname of server, all alias list, list of IP addr which can be used to reach it. this can help a client implement their own load balancing as they know all the ips to reach the server
  - Use ```getfqdn()``` to convert partial to fully qualified domain name
  - Use ```gethostbyaddr("<IP>")``` to get hostname from given servers IP. returns hostname, alias list, all IPs list

### Service Info
  - ```getservbyname("<URL>")``` gives you the port number of network service with standardized name. eg: 
    ```
    from urllib.parse import urlparse
    socket.getservbyname("https://www.python.org")

    > https : 443
    ```
  - Use ```getservbyport(<num>)``` reverse port lookup. eg:
    ```
    url = '{}://example.com/'.format(socket.getservbyport(80))
    print(url)

    > http://example.com
    ```
  - Useful code:
    ```python
    import socket
    list1 = dir(socket)  # returns list of all methods and attr of an obj
    attr_dict = {getattr(socket,n):n for n in list1 if n.startswith('IPPORTO_')}  # creates a dict having the proto names which start with IPPROTO, and their transport protocol number
    ``` 
  - Use ```getprotobyname('<proto>')``` to transport proto num assigned to a protocol

