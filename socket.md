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
    def get_constants(string):
        return {                                                                # returns a dict having transport proto num of proto which start with IPPROTO_, and the proto name
            getattr(socket,n):n for n in dir(socket) if n.startswith(string)    # dir(socket) returns list of all methods and attr of an obj
    }
    ip_proto_dict = get_constants('IPPROTO_')
    ``` 
  - Use ```getprotobyname('<proto>')``` to transport proto num assigned to a protocol

### Lookup Server Address
  - ```getaddrinfo("<server>", "<port>" [,optional])``` returns list of tuples containing info to make a conn. layout of a tuple is: addr family, socktype, protocol num, cannonical name, sock addr.
    server and port are compulsory to pass to the function, but there are optional perimeters too, which are family, socktype, proto, flags. eg:
    ```
    In [23]: socket.getaddrinfo('www.python.org','http')
    Out[23]:
            [(<AddressFamily.AF_INET: 2>,
            <SocketKind.SOCK_STREAM: 1>,
            6,
            '',
            ('151.101.152.223', 80)),
            (<AddressFamily.AF_INET6: 10>,
            <SocketKind.SOCK_STREAM: 1>,
            6,
            '',
            ('2a04:4e42:24::223', 80, 0, 0))]
    ```

### IP Addr Representations
  - in C, datatype *struct sockaddr* used to represent IP as binary value, unlike python
  - to convert IP from python to C representation and vice versa, use ```inet_aton()``` (ascii to network-byte, so from python to C type format) and ```inet_ntoa()``` (ntoa means network-byte to ascii, so from C to python type format). eg:
    ```
    socket.inet_aton('127.0.0.1')
    >  b'\x7f\x00\x00\x01'

    socket.inet_ntoa(b'\x7f\x00\x00\x01')
    > '127.0.0.1'
    ```
  - ```inet_ntop()``` and ```inet_pton()``` take in both the string/byte-format and the addr type (AF_INET or AF_INET6). eg:
    ```
    socket.inet_pton(socket.AF_INET6,'2002:ac10:10a:1234:21e:52ff:fe74:40e')
    > b' \x02\xac\x10\x01\n\x124\x02\x1eR\xff\xfet\x04\x0e'

    socket.inet_ntop(socket.AF_INET6, b' \x02\xac\x10\x01\n\x124\x02\x1eR\xff\xfet\x04\x0e')
    > '2002:ac10:10a:1234:21e:52ff:fe74:40e'
    ```
################ END FOR NOW ################ 
