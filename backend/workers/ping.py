import time
import os
import subprocess, platform



def ping(q, ip):
    """
    Returns True and latency if host responds to a ping request
    """
    if platform.system().lower()=="windows":
        cmd = ["ping", ip, "-t"]
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            ping_dict = {}
            if stdout_line[:5] == "Reply":
                try:
                    latency = stdout_line.split()[4].split('=')[1][:-2]
                    ping_dict['host'] = ip
                    ping_dict['latency'] = latency
                    ping_dict['response'] = True
                except IndexError:
                    ping_dict['host'] = ip
                    ping_dict['latency'] = 999
                    ping_dict['response'] = False
            elif stdout_line[:7] == "Request":
                ping_dict['host'] = ip
                ping_dict['latency'] = 999
                ping_dict['response'] = False
            q.put({'gateway' : ping_dict})

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


if __name__ == '__main__':
    import multiprocessing

    ip = '10.221.64.1'

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=ping, args=(q, ip, ))
    p.start()

    while True:
        line = q.get()
        print(line)

# python ./backend/workers/ping.py