"""
Lakitu daemon class definition
"""
import pygst
pygst.require('0.10')
import gst
import getpass
import soundcloud

# LakituDaemon class definition
class LakituDaemon(object):
    def __init__(self, username):
        """Creates a new Lakitu daemon instance"""
        self._client = self.connect(username)

        # Load initial initial tracklist
        feed = self._client.get('/me/activities')

        self._playlist = [x for x in feed.collection if x['type'] == 'track']
        self._next_href = feed.next_href
        self._future_href = feed.future_href

    def connect(self, username):
        """Connects to SoundCloud"""
        password = getpass.getpass()

        print("Connecting to SoundCloud...")
        client = soundcloud.Client(client_id='bf7b52c22edb1f76847539356ec563d9',
                                   client_secret='b4f0501fd039e73d45883d3f2fbe6ec7',
                                   username=username,
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
