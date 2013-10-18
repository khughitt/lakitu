#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Lakitu SoundCloud client
2013/10/14
"""
import sys
import locale
import curses
import curses.wrapper
import Pyro4.core

def main(screen):
    """Main"""
    # Set locale
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE) 
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)

    # connect to pyro
    lak = Pyro4.Proxy(sys.argv[1])

    # load tracklist
    playlist = lak.get_tracklist()
    #for track in playlist:
    #    text = track['origin']['title'].encode(code)
    #    screen.addstr(text, curses.color_pair(0))
    #    #screen.addstr("\n")

    #screen.bkgd(curses.color_pair(1))
    screen.refresh()

    # Main loop
    while 1:
        c = screen.getch()
        if c == ord('n'):
            screen.addstr("Next track", curses.color_pair(2))
            lak.next()
        if c == ord('p'):
            screen.addstr("Previous track", curses.color_pair(2))
            lak.prev()
        elif c == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
