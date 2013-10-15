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
# http://stackoverflow.com/questions/656933/communicating-with-a-running-python-daemon
#
import soundcloud
import pygst
pygst.require('0.10')
import gst
import getpass
import warnings
import Pyro4.core

# Lakitu class definition
class Lakitu(object):
    def __init__(self):
        """Creates a new Lakitu daemon instance"""
        self._client = self.connect()

        # Load initial initial tracklist
        feed = self._client.get('/me/activities')

        self._playlist = [x for x in feed.collection if x['type'] == 'track']
        self._next_href = feed.next_href
        self._future_href = feed.future_href

    def connect(self):
        """Connects to SoundCloud"""
        password = getpass.getpass()

        print("Connecting to SoundCloud...")
        client = soundcloud.Client(client_id='bf7b52c22edb1f76847539356ec563d9',
                                   client_secret='b4f0501fd039e73d45883d3f2fbe6ec7',
                                   username='user549420240',
                                   password=password)
        return client

    def get_tracklist(self):
        """Returns a list of tracks currently queued up"""
        return self._playlist

    def play(self):
        """Begin playing a user's audio stream"""
        print("Playing " + self._playlist[0]['origin']['title'])

        track = self._client.get(self._playlist[0]['origin']['uri'])
        stream_url = self._client.get(track.stream_url, allow_redirects=False)

        #mainloop = gobject.MainLoop()
        pl = gst.element_factory_make("playbin2", "player")
        pl.set_property('uri', stream_url.location)
        pl.set_state(gst.STATE_PLAYING)

# Initialize Pyro server
lakitu = Lakitu()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    daemon = Pyro4.Daemon()
    uri = daemon.register(lakitu)
    print("Started Pyro instance at %s" % daemon.locationStr)
    print("uri: %s" % uri)
    lakitu.play()
    daemon.requestLoop()

#mainloop.run()
#pl.set_state(gst.STATE_PAUSED)
