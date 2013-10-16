#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
A Simple SoundCloud Player (testing)
Keith Hughitt (keith.hughitt@gmail.com)
2013/10/12

References:
-----------
* http://guzalexander.com/2012/08/17/playing-a-sound-with-python.html
* http://developers.soundcloud.com/docs#playing
* http://stackoverflow.com/questions/656933/communicating-with-a-running-python-daemon
"""
import sys
import Pyro4.core
import warnings
import lakitu

def main():
    """Main"""
    # Initialize Pyro server
    lakitu = lakitu.daemon.LakituDaemon('user549420240')

    # We are just going to run locally so we can ignore Pyro4 warnings for now.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        daemon = Pyro4.Daemon()
        uri = daemon.register(lakitu)
        print("Started Pyro instance at %s" % daemon.locationStr)
        print("uri: %s" % uri)
        lakitu.play()
        daemon.requestLoop()

    #pl.set_state(gst.STATE_PAUSED)

if __name__ == "__main__":
    sys.exit(main())
