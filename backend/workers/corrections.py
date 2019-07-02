import socket
import time



def listen(q, bind, source, port):

    corrections_dict = {
        'correctionsSec' : 0,
        'correctionsMin' : 0,
        'correctionsTot' : 0
    }

    while True:
        try:
            # Open socket once (i.e not for each thread)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Set socket buffer options
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8388608)
            # Bind to ip and port
            s.bind((bind, int(port)))
            break
        except:
            q.put(corrections_dict)
            time.sleep(1)




    start_time = time.time()
    correctionsTotal = 1
    
    while True:
        try:
            elapsed = time.time()+0.1 - start_time
            corrections_dict['elapsed'] = round(elapsed, 2)

            s.settimeout(1.1)
            data, addr = s.recvfrom(32768)

            
            if addr[0] == source:
                correctionsTotal += 1
                corrections_dict['correctionsSec'] = round(correctionsTotal / elapsed, 2)
                corrections_dict['correctionsMin'] = round(correctionsTotal / (elapsed/60), 2)
                corrections_dict['correctionsTot'] = round(correctionsTotal, 2)
        except:
            pass
            
        q.put({'corrections': corrections_dict})
   

    
if __name__ == '__main__':
    import multiprocessing
    
    bind = '10.221.64.123'
    source = '10.221.64.7'
    port = '3784'
    
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=listen, args=(q, bind, source, port, ))
    p.start()
    
    while True:
        line = q.get()
        print(line)

# python ./backend/tests/corrections.py