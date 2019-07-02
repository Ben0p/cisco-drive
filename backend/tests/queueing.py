import multiprocessing
import random
import time

def f(q):
    while True:
        rn = random.randint(1, 100)
        q.put([rn, None, 'hello'])
        time.sleep(0.2)

def g(q):
    while True:
        rn = random.randint(1, 100)
        q.put([rn, None, 'goodbye'])
        time.sleep(1.2)

if __name__ == '__main__':
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=f, args=(q,))
    r = multiprocessing.Process(target=g, args=(q,))
    p.start()
    r.start()
    while True:
        line = q.get()
        if line[2] == 'hello':
            print('{} = {}'.format(line[2], line[0]))
        elif line[2] == 'goodbye':
            print('{} = {}'.format(line[2], line[0]))



# python ./backend/tests/queueing.py