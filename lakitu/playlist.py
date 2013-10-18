"""
Soundcloud-related classes
"""

class PlayList(object):
    """Soundcloud playlist"""
    def __init__(self, feed):
        """Creates a new PlayList instance"""
        # Filter out non-tracks
        self._tracks = [x for x in feed.collection if x['type'] == 'track']
        self._num = 0

    def current(self):
        """Returns the currently selected track"""
        return self._tracks[self._num]

    def next(self):
        """Returns the next track in the playlist"""
        self._num = min(len(self._tracks) - 1, self._num + 1)
        return self._tracks[self._num]

    def prev(self):
        """Returns the previous track in the playlist"""
        self._num = max(0, self._num - 1)
        return self._tracks[self._num]

# May use in future...
class Track(object):
    """Soundcloud track"""
    def __init__(self, track_dict):
        """Creates a new Track instance"""
        self._raw = track_dict

        self.description = track['description']
        self.duration = track['duration']
        self.id = track['id']
        self.stream_url = track['stream_url']
