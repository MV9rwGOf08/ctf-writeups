# Copy-pasted from SGLE: https://github.com/pauloklaus/sgle-game/

import curses
from curses import KEY_RIGHT, KEY_LEFT

import time

if __name__ == '__main__':
    curses.initscr()
    window = curses.newwin(15, 40, 0, 0)
    window.timeout(20)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
    while True:
        event = window.getch()
        if event == -1:
            continue
        print event, event == KEY_LEFT
    # time.sleep(10)
    curses.endwin()
