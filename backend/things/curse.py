import curses
from things import asciiart



class display():
    '''
    Curses display for the current statistics
    '''

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.ascii_art = asciiart.asciiArt()


    def screen(self, master, _uptime):
        # Clear the screen
        self.stdscr.clear()

        # Create a boarder
        self.stdscr.border(0)

        # Title
        self.stdscr.addstr(0,2,"Cisco Drive")

        # Position windows
        self.box1 = curses.newwin(3, 28, 1, 29) # Top middle (uptime)
        self.box2 = curses.newwin(5, 28, 4, 1) # Middle left (corrections in)
        self.box3 = curses.newwin(5, 28, 4, 29) # Middle middle (corrections out)
        self.box4 = curses.newwin(5, 28, 4, 57) # Middle right (corrections sent)
        self.box5 = curses.newwin(4, 28, 9, 1) # Bottom left (list)
        self.box6 = curses.newwin(4, 28, 9, 29) # Bottom middle (binding)
        self.box7 = curses.newwin(4, 28, 9, 57) # Bottom right (buffer)
        #self.box8 = curses.newwin(3, 28, 1, 1) # Top Left (warning)
        #self.box9 = curses.newwin(3, 28, 1, 57) # Top Right (delay)
        self.box10 = curses.newwin(10, 28, 13, 29) # Bottom (ascii art)


        # Create boarder box's
        self.box1.box()
        self.box2.box()
        self.box3.box()
        self.box4.box()
        self.box5.box()
        self.box6.box()
        self.box7.box()
        #self.box8.box()
        #self.box9.box()
        self.box10.box()


        # Titles of the windows
        self.box1.addstr(0,2,"Run Time")
        self.box2.addstr(0,2,"AP")
        self.box3.addstr(0,2,"AMPs")
        self.box4.addstr(0,2,"zLIBs")
        self.box5.addstr(0,2,"Position")
        self.box6.addstr(0,2,"Gateway")
        self.box7.addstr(0,2,"Corrections")
        #self.box8.addstr(0,10,"Nothing")
        #self.box9.addstr(0,12,"Nothing")
        self.box10.addstr(0,2,"Look out for ROBOTS")

        # Contents of each window
        self.box1.addstr(1,1,' '*26)
        self.box1.addstr(1,1,_uptime.center(26, ' '))


        self.box2.addstr(1,1,' Hostname: {}'.format(master['wgb']['hostname']))
        self.box2.addstr(2,1,'     RSSI: {}dBm'.format(master['wgb']['rssi']))
        self.box2.addstr(3,1,'      SNR: {}dBm'.format(master['wgb']['snr']))


        self.box3.addstr(1,1,' AMPs/Sec: {}'.format(master['mcast']['ampsSec']))
        self.box3.addstr(2,1,' AMPs/Min: {}'.format(master['mcast']['ampsMin']))
        self.box3.addstr(3,1,' AMPs/Tot: {}'.format(master['mcast']['ampsTot']))

        self.box4.addstr(1,1,' ZLIBs/Sec: {}'.format(master['mcast']['zlibSec']))
        self.box4.addstr(2,1,' ZLIBs/Min: {}'.format(master['mcast']['zlibMin']))
        self.box4.addstr(3,1,' ZLIBs/Tot: {}'.format(master['mcast']['zlibTot']))

        if master['him']['latitude']:
            lat = round(float(master['him']['latitude']), 8)
        else:
            lat = ''
        if master['him']['longitude']:
            lon = round(float(master['him']['longitude']), 8)
        else:
            lon = ''

        self.box5.addstr(1,1,'  Latitude: {}'.format(lat))
        self.box5.addstr(2,1,' Longitude: {}'.format(lon))

        self.box6.addstr(1,1,' Gateway: {}'.format(master['gateway']['host']))
        self.box6.addstr(2,1,' Latency: {}ms'.format(master['gateway']['latency']))

        self.box7.addstr(1,1,'Corrections/Sec: {}'.format(master['corrections']['correctionsSec']))
        self.box7.addstr(2,1,'Corrections/Min: {}'.format(master['corrections']['correctionsMin']))

        #self.box8.addstr(1,1,' '*26)
        ##self.box8.addstr(1,1,'DO NOT CLOSE'.center(26, ' '), curses.color_pair(1))

        #self.box9.addstr(1,1,' '*26)
        ##self.box9.addstr(1,1,str(master['him']['device']).center(26, ' '))


        # Ascii window
        self.box10.addstr(1,10,"   T")
        self.box10.addstr(2,10,' .-"-.')
        self.box10.addstr(3,10,'|  ___|')
        self.box10.addstr(4,10,'| (.\/.)')
        self.box10.addstr(5,10,"|  ,,,' ")
        self.box10.addstr(6,10,"| '###")
        self.box10.addstr(7,10," '----'")

        
        # Refresh whole screen and each window
        self.stdscr.refresh()
        self.box1.refresh()
        self.box2.refresh()
        self.box3.refresh()
        self.box4.refresh()
        self.box5.refresh()
        self.box6.refresh()
        self.box7.refresh()
        #self.box8.refresh()
        #self.box9.refresh()
        self.box10.refresh()
