from pygame.mixer import music
import os
import sys

GAME_DIR = os.path.dirname(os.path.abspath(sys.argv[0])) + "/../"
MUSIC_PATH = GAME_DIR + "/etc/sound/"


def play(song, loops=-1, start=0.0):
    volume = get_volume()
    if music.get_busy():
        fadeout(1000)
    music.load(MUSIC_PATH + song)
    music.play(loops, start)
    set_volume(volume)


def instant_play(song, loops=-1, start=0.0):
    volume = get_volume()
    music.stop()
    music.load(MUSIC_PATH + song)
    music.play(loops, start)
    set_volume(volume)


def fadeout(time):
    music.fadeout(time)


def queue(song):
    music.queue(MUSIC_PATH + song)


def replay(loops=-1, start=0.0):
    music.play(loops, start)


def pause():
    music.pause()


def resume():
    music.unpause()


def get_volume():
    return music.get_volume()

def set_volume(value):
    return music.set_volume(value)


def stop():
    music.stop()


def is_playing(song=None):
    if song:
        pass
    return music.get_busy()
