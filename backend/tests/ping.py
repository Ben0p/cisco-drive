import time
import os
import subprocess, platform



def ping(host):
    """
    Returns True and latency if host responds to a ping request
    """
    if platform.system().lower()=="windows":
        cmd = ["ping", host, "-t"]
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            if stdout_line[:5] == "Reply":
                try:
                    yield(stdout_line.split()[4].split('=')[1][:-2], True)
                except IndexError:
                    yield(999, False)
            elif stdout_line[:7] == "Request":
                yield(999, False)

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    else:
                
        cmd = ['ping', host]
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            if stdout_line[:2] == "64":
                try:
                    yield(stdout_line.split()[6].split('=')[1][:-3], True)
                except IndexError:
                    yield(999, False)
            elif stdout_line[:4] == "From":
                yield(999, False)
            else:
                yield(999, False)

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)



if __name__ == '__main__':
    while True:
        for pong, online in ping('10.221.64.1'):
            print(pong+'ms')