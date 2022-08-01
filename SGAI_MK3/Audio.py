from pymediainfo import MediaInfo
from ffpyplayer.player import MediaPlayer
from os.path import exists, basename, splitext
import time
class Audio:
    def __init__(self, filePath, volume = 1):
        self.filePath = filePath
        aud = MediaPlayer(filePath)
        aud.set_volume(volume)
        print(aud.get_volume())
        self.audio = aud
        info = MediaInfo.parse(self.filePath).audio_tracks[0]
        self.duration = info.duration / 1000
        self.startTime = time.process_time()
        self.endTime = self.duration + self.startTime