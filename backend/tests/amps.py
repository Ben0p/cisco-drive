import socket
import binascii
import re
import time

def listen(q):
  amps_dict = {}
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



  start_time = time.time()
  amps_tot = 1
  zlib_tot = 1

  while True:

    elapsed = time.time()+0.1 - start_time

    amps_dict['elapsed'] = round(elapsed, 2)

    data, addr = sock.recvfrom(2048)
    length = len(data)


    if length > 1000:
      amps_tot += 1
    elif length < 1000:
      zlib_tot += 1

    
    amps_dict['ampsSec'] = round(amps_tot / elapsed, 2)
    amps_dict['zlibSec'] = round(zlib_tot / elapsed, 2)

    amps_dict['ampsMin'] = round(amps_tot / (elapsed/60), 2)
    amps_dict['zlibMin'] = round(zlib_tot / (elapsed/60), 2)

    amps_dict['ampsTot'] = round(amps_tot, 2)
    amps_dict['zlibTot'] = round(zlib_tot, 2)

    q.put(amps_dict)
   

    
if __name__ == '__main__':
    import multiprocessing

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=listen, args=(q, ))
    p.start()

    while True:
        line = q.get()
        print(line)

# python ./backend/tests/amps.py