#!/usr/bin/env python
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
import os
import Pyro4.core
import warnings
import lakitu

def main():
    """Main"""
    # Initialize Pyro server
    lak = lakitu.daemon.LakituDaemon('user549420240')

    # We are just going to run locally so we can ignore Pyro4 warnings for now.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        daemon = Pyro4.Daemon()

    uri = daemon.register(lak)
    print("Started Pyro instance at %s" % daemon.locationStr)
    print("uri: %s" % uri)
    store_uri(uri)

    # Begin playing stream
    lak.play()
    daemon.requestLoop()

def store_uri(uri):
    """Stores the Pyro instance URI in an accessible location"""
    # Determine location for lakitu configuration
    config_dir = (os.getenv('XDG_CONFIG_HOME') or 
                  os.path.join(os.getenv('HOME'), '.config'))
    config_dir = os.path.join(config_dir, 'lakitu')

    config_file = os.path.join(config_dir, '.session')

    # Create config dir if it doesn't already exist
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir, 0o755)

    # Store uri
    with open(config_file, 'w') as fp:
        fp.write(str(uri))

if __name__ == "__main__":
    sys.exit(main())
