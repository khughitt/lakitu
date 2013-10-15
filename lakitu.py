#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# A Simple SoundCloud Player (testing)
# Keith Hughitt (keith.hughitt@gmail.com)
# 2013/10/12
#
# References:
# http://guzalexander.com/2012/08/17/playing-a-sound-with-python.html
# http://developers.soundcloud.com/docs#playing
#
import soundcloud
import pygst
pygst.require('0.10')
import gst
#import gobject
import curses
import getpass
import sys
import os

password = getpass.getpass()

print("Connecting to SoundCloud...")
client = soundcloud.Client(client_id='bf7b52c22edb1f76847539356ec563d9',
                           client_secret='b4f0501fd039e73d45883d3f2fbe6ec7',
                           username='user549420240',
                           password=password)

latest = client.get('/me/activities')
print("Playing " + latest.collection[0]['origin']['title'])

track = client.get(latest.collection[0]['origin']['uri'])
stream_url = client.get(track.stream_url, allow_redirects=False)

#mainloop = gobject.MainLoop()
pl = gst.element_factory_make("playbin2", "player")
pl.set_property('uri', stream_url.location)
pl.set_state(gst.STATE_PLAYING)

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

#mainloop.run()
#pl.set_state(gst.STATE_PAUSED)
