import curses
import time
import random



class display():
    '''
    Curses display for the current statistics
    '''

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)


    def screen(self):
        # Clear the screen
        self.stdscr.clear()

        # Create a boarder
        self.stdscr.border(0)

        # Title
        self.stdscr.addstr(0,32,"Cisco Drive")

        # Position windows
        self.box1 = curses.newwin(3, 28, 1, 29) # Top middle (uptime)

        # Create boarder box's
        self.box1.box()


        # Titles of the windows
        self.box1.addstr(0,11,"Random Number")


        # Contents of each window
        self.box1.addstr(1,1, str(random.randint(0,100000000)))
        
        # Refresh whole screen and each window
        self.stdscr.refresh()
        self.box1.refresh()



if __name__ == '__main__':


    _display = display()

    while True:
         _display.screen()
         time.sleep(1)

            

                

# python ./backend/tests/curse.py