import socket
import serial
from multiprocessing import Process
import time
from ping import ping


def corrections():
    # Corrections settings receiving broadcast
    corrections = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    corrections.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    corrections.bind(('', 3784))
    corrections.settimeout(1.1)

    while True:    
        try:
            data, addr = corrections.recvfrom(1024)
            print(addr[0])
        except:
            print('Expection')

def amps():
    # Receiving AMPS multicast
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
        try:
            data, addr = sock.recvfrom(2048)
            print(addr[0])
        except:
            print('Expection')


def latency(host):
    while True:
        for pong, online in ping('10.221.64.1'):
            print(pong+'ms')

if __name__ == '__main__':

    t = Process(target=amps)
    t.daemon = True
    t.start()

    p = Process(target=latency, args=('10.221.64.1',))
    p.daemon = True
    p.start()

    corrections()