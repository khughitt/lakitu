"""
Lakitu daemon class definition
"""
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import getpass
import soundcloud
from lakitu.playlist import PlayList

# LakituDaemon class definition
class LakituDaemon(object):
    def __init__(self, username):
        """Creates a new Lakitu daemon instance"""
        self._client = self.connect(username)

        # Initialize Gstreamer
        GObject.threads_init()
        Gst.init(None)
        self._player = Gst.ElementFactory.make('playbin', None)

        # Load initial initial tracklist
        feed = self._client.get('/me/activities')

        self._playlist = PlayList(feed)
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
        self._play(self._playlist.current())

    def _stop(self):
        self._player.set_state(Gst.State.PAUSED)

    def _play(self, track):
        print("Playing " + track['origin']['title'])
        track_info = self._client.get(track['origin']['uri'])
        stream_url = self._client.get(track_info.stream_url,
                                      allow_redirects=False)

        self._player.set_property('uri', stream_url.location)
        self._player.set_state(Gst.State.PLAYING)

    def next(self):
        """Play the next track"""
        self._play(self._playlist.next())

    def prev(self):
        """Play the previous track"""
        self._play(self._playlist.prev())

