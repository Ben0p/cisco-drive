import paramiko
import time


def wgb(q, ip, un, pw):
    wgb_stats = {
        'response' : False,
        'mac' :'',
        'hostname' : '',
        'ip' : '',
        'rssi' : '',
        'snr' : ''
        }
    unresponsive = 0

    while True:
        while True:
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                client.connect(ip, port=22, username=un, password=pw)
                connection = client.invoke_shell()
                connection.send("\n")
                time.sleep(1)
                break
            except:
                wgb_stats['response'] = False
                q.put(wgb_stats)
                time.sleep(1)

        while True:
            wgb_stats = {
                'response' : False,
                'mac' :'',
                'hostname' : '',
                'ip' : '',
                'rssi' : '',
                'snr' : ''
        }
            try:
                connection.send('show dot11 associations all-client\n')
                time.sleep(1)
                connection.send(' ')
                time.sleep(1)
                connection.send('\n')
                time.sleep(1)
                file_output = connection.recv(9999).decode(encoding='utf-8')
                wgb_stats['response'] = True
                lines = file_output.splitlines()
                for line in lines:
                    if line.startswith('Address'):
                        ap_mac_a = line.split(':')[1].strip()
                        ap_mac = ap_mac_a.split()[0].strip()
                        ap_hostname = line.split(':')[2].strip()
                        wgb_stats['mac'] = ap_mac
                        wgb_stats['hostname'] = ap_hostname
                    elif line.startswith('IP Address'):
                        address = line.split(':')[1].strip()
                        ap_ip = address.split()[0].strip()
                        wgb_stats['ip'] = ap_ip
                    elif line.startswith('Signal Strength'):
                        signal = line.split(':')[1]
                        rssi = signal.split()[0].strip()
                        wgb_stats['rssi'] = rssi
                    elif line.startswith('Signal to Noise'):
                        noise = line.split(':')[1]
                        snr = noise.split()[0].strip()
                        wgb_stats['snr'] = snr
                if len(wgb_stats) < 1:
                    wgb_stats['response'] = False
                unresponsive = 0

            except:
                wgb_stats['resonse'] = False
                connection.send('\n')
                connection.send('\n')
                connection.send('\n')

                unresponsive += 1
                if unresponsive >= 5:
                    break


            q.put({'wgb' : wgb_stats})
            time.sleep(1)

            

if __name__ == '__main__':
    import multiprocessing

    ip = '10.221.69.51'
    un = 'bgorham'
    pw = 'xxx'

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=wgb, args=(q, ip, un, pw))
    p.start()

    while True:
        line = q.get()
        print(line)




# python ./backend/workers/ssh.py