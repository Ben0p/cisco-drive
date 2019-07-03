import multiprocessing
from workers import him, mcast, ping, ssh, corrections
import threading
import time
from things import asciiart, uptime, curse
from datetime import datetime
import os
import getpass



# Master Dictionary

master = {
    'him' : {
        'device':'',
        'ip':'',
        'easting':'',
        'northing':'',
        'elevation':'',
        'latitude':'-22.00000000',
        'longitude':'119.00000000',
        'response':''
    },
    'mcast' : {
        'ampsSec' : '',
        'zlibSec' : '',
        'ampsMin' : '',
        'zlibMin' : '',
        'ampsTot' : '',
        'zlibTot' : ''
    },
    'gateway' : {
        'host' : '',
        'latency' : '',
        'response' : ''
    },
    'wgb' : {
        'mac' : '',
        'hostname' : '',
        'ip' : '',
        'rssi' : '',
        'snr' : '',
        'response' : ''
    },
    'corrections' : {
        'correctionsSec' : 0,
        'correctionsMin' : 0,
        'correctionsTot' : 0
    }
}

_uptime = ''
timestamp = time.time()
filetime = datetime.now().strftime('%Y%m%d%H%M%S')



if __name__ == '__main__':

    # Fix PyInstaller bug
    multiprocessing.freeze_support()
    
    gateway = '10.221.64.1'
    un = input("FMGOPS Username: ")
    pw = getpass.getpass()
    him_ip = input("IP of HIM: ")
    wgb_ip = input("IP of WGB: ")
    tab_ip = input("IP of Tablet: ")
    '''
    un = 'bgorham'
    pw = 'xxx'
    him_ip = '10.221.69.53'
    wgb_ip = '10.221.69.51'
    tab_ip = '10.221.64.123'
    '''
    bcast_port = '3784'
    base = '10.221.64.7'

 

    # Initiate queue
    q = multiprocessing.Queue()

    # Setup HIM scraping
    him_location = multiprocessing.Process(target=him.scrape, args=(q, him_ip, ))
    him_location.start()

    # Setup Multicast listening
    multicast = multiprocessing.Process(target=mcast.listen, args=(q, tab_ip))
    multicast.start()

    # Setup gateway ping process
    ping_gateway = multiprocessing.Process(target=ping.ping, args=(q, gateway, ))
    ping_gateway.start()

    # Setup gateway ping process
    wgb = multiprocessing.Process(target=ssh.wgb, args=(q, wgb_ip, un, pw, ))
    wgb.start()

    # Setup gateway ping process
    bcast = multiprocessing.Process(target=corrections.listen, args=(q, tab_ip, base, bcast_port, ))
    bcast.start()


    one_sec = 0
    start = time.time()


    # Create directories
    if not os.path.exists('output'):
        os.makedirs('output')

    with open('output/{}.csv'.format(filetime), 'w', 10) as f:

        _display = curse.display()

        while True:
            line = q.get()

            for akey, avalue in line.items():
                for bkey, bvalue in avalue.items():
                    master[akey][bkey] = bvalue


            if one_sec == 0:
                one_sec = time.time() - start
            elif 0 < one_sec < 1:
                one_sec =  time.time() - start
            elif one_sec > 1:
                start = time.time()
                one_sec = 0
                f.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                    round(time.time(), 2),
                    master['him']['device'],
                    master['him']['ip'],
                    master['him']['easting'],
                    master['him']['northing'],
                    master['him']['elevation'],
                    master['him']['latitude'],
                    master['him']['longitude'],
                    master['him']['response'],
                    master['mcast']['ampsSec'],
                    master['mcast']['zlibSec'],
                    master['mcast']['ampsMin'],
                    master['mcast']['zlibMin'],
                    master['mcast']['ampsTot'],
                    master['mcast']['zlibTot'],
                    master['gateway']['host'],
                    master['gateway']['latency'],
                    master['gateway']['response'],
                    master['wgb']['mac'],
                    master['wgb']['hostname'],
                    master['wgb']['ip'],
                    master['wgb']['rssi'],
                    master['wgb']['snr'],
                    master['wgb']['response'],
                    master['corrections']['correctionsSec'],
                    master['corrections']['correctionsMin'],
                    master['corrections']['correctionsTot']
                    ))
                uptime_seconds = time.time()-timestamp
                _uptime = uptime.uptime(uptime_seconds)
    

                _display.screen(master, _uptime)


            
            

                

# python ./backend/run.py