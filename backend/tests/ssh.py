import paramiko
import time



client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('10.221.64.19', port=22, username='bgorham', password='xxx')
connection = client.invoke_shell()
connection.send("\n")
time.sleep(1)

while True:
    connection.send('show dot11 associations all-client\n')
    time.sleep(1)
    connection.send(' ')
    time.sleep(1)
    connection.send('\n')
    time.sleep(1)
    file_output = connection.recv(9999).decode(encoding='utf-8')
    lines = file_output.splitlines()
    for line in lines:
        if line.startswith('Address'):
            ap_mac_a = line.split(':')[1].strip()
            ap_mac = ap_mac_a.split()[0].strip()
            ap_hostname = line.split(':')[2].strip()
            print(ap_hostname)
            print(ap_mac)
        elif line.startswith('IP Address'):
            address = line.split(':')[1].strip()
            ap_ip = address.split()[0].strip()
            print(ap_ip)
        elif line.startswith('Signal Strength'):
            signal = line.split(':')[1]
            rssi = signal.split()[0].strip()
            print(rssi)
        elif line.startswith('Signal to Noise'):
            noise = line.split(':')[1]
            snr = noise.split()[0].strip()
            print(snr)

            





# python ./backend/tests/ssh.py