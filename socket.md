notes made from https://pymotw.com/3/socket  

sockets:
  - an endpoint of a comminication channel used by prog to pass data back and forth
  - two properties controlling the way they send data:
    - address family: controls network layer protocol
    - socket type: controls transport layer protocol

python has 3 address famimlies:
  - AF_INET: for ipv4 addressing, takes ip in the format x.x.x.x
  - AF_INET6: for ipv6 addressing
  - AF_UNIX: address family for Unix Domain Sockets (UDS), which is an IPC protocol. its implementation allows data passing directly between processes, without going through network stack. restricted to processes on the same system. is more effective than AF_INET

socket type is usually SOCK_DGRAM for message oriented datagram transport or SOCK_STREAM for stream oriented.
datagram sockets are usually associated with UDP, and stream sockets with TCP.
for reliable, in order delivery needed - TCP handles automatically
for delivery where order not important, small messages, or multicasting - UDP


