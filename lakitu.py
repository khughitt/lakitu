#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Lakitu SoundCloud client
2013/10/14
"""
import sys
import curses

screen = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
screen.keypad(1)

# Main loop
while 1:
    c = screen.getch()
    if c == ord('n'):
        screen.addstr("Next track", curses.color_pair(2))
    elif c == ord('q'):
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
        sys.exit()

