#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Lakitu SoundCloud client
2013/10/14
"""
import sys
import urwid
import Pyro4.core

class Lakitu(object):
    """Lakitu class definition"""
    def __init__(self, uri):
        """Create a new Lakitu instance"""
        # connect to pyro
        self.lak = Pyro4.Proxy(uri)

        # load tracklist
        playlist = self.lak.get_tracklist()
        #for track in playlist:
        #    text = track['origin']['title'].encode(code)
        #    screen.addstr(text, curses.color_pair(0))
        #    #screen.addstr("\n")
        blank = urwid.Divider()

        listbox_content = [
            blank,
            urwid.Text(u"Entry 1"),
            blank,
            urwid.Text(u"Entry 2")
        ]

        header = urwid.AttrWrap(urwid.Text(u"Lakitu"), 'header')
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)

        # Colors
        palette = [
            ('body', 'dark magenta', 'light blue', 'standout'),
            ('reverse', 'light blue', 'dark magenta'),
            ('header', 'light magenta', 'dark blue', 'bold')
            ]

        #filler = urwid.Filler(urwid.Text(u"Lakitu"), 'top')
        loop = urwid.MainLoop(frame, palette, 
                              unhandled_input=self._parse_input)
        loop.run()

    def _parse_input(self, key):
        """Main execution loop"""
        c = key.lower()

        if c == 'n':
            #screen.addstr("Next track", curses.color_pair(2))
            self.lak.next()
        if c == 'p':
            #screen.addstr("Previous track", curses.color_pair(2))
            self.lak.prev()
        if c == 'q':
            raise urwid.ExitMainLoop()


if __name__ == "__main__":
    uri = sys.argv[1]
    app = Lakitu(uri)
