import socket
import binascii
import re

def main():
  MCAST_GRP = '224.100.100.110' 
  MCAST_PORT = 13001
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  except AttributeError:
    pass
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

  sock.bind(('', MCAST_PORT))
  host = '10.221.64.123'
  sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
  sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, 
                   socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

  while True:

    data, addr = sock.recvfrom(2048)

    string = data.decode("utf-8", errors='ignore') 

    print(string)

    
if __name__ == '__main__':
  main()