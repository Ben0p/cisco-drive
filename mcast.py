import socket
import struct
import sys

multicast_group = '224.100.100.110'
server_address = ('', 13001)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

# Receive/respond loop
while True:
    try:
        data, address = sock.recvfrom(1024)
        print(address[0])
        print('sending acknowledgement to', address)
        sock.sendto('ack', address)
    except:
        print('\nwaiting to receive message')
    