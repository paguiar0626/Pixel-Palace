# pylint: disable="global-statement"

import random
from enum import Enum

from pygame import mixer

from save_data_manager import Data, SaveDataManager

save_data_manager = SaveDataManager()

BASE_PATH = "assets/sounds"

all_music = [
    "chill-lofi-song.mp3",
    "deep-in-manhattan.mp3",
    "swing.mp3",
]
previous_track = ""

music_volume: float = save_data_manager.load(Data.music_volume, 0.25)
sfx_volume: float = save_data_manager.load(Data.sfx_volume, 1.0)


class Sounds(Enum):
    """Maps a sound effect to its filepath."""
    generic_button = f"{BASE_PATH}/coin.wav"
    game_over = f"{BASE_PATH}/negative.wav"
    # add more sound effects here as needed


def play(sound_name: Sounds) -> None:
    """Play a sound effect.

    Args:
        sound_name: a member of the Sounds enum
    """
    mixer.Channel(0).set_volume(sfx_volume)
    mixer.Channel(0).play(mixer.Sound(sound_name.value))


def play_background_music() -> None:
    """Play background music from a predetermined set of tracks."""
    # The music is pretty loud by default, so halve the volume passed to the mixer
    mixer.music.set_volume(music_volume / 2)

    if mixer.music.get_busy():
        return

    global previous_track
    available_music = [
        track for track in all_music if track != previous_track
    ]
    next_track = random.choice(available_music)

    mixer.music.load(f"{BASE_PATH}/{next_track}")
    mixer.music.play(fade_ms=2000)

    previous_track = next_track


def clamp(n, min_, max_):
    """Ensure that a value falls between a specified min and max range."""
    return max(min(max_, n), min_)


def change_music_volume(delta: float) -> None:
    """Increase or decrease the music volume by a specified amount.

    Args:
        delta: the value by which to change the music volume
    """
    global music_volume
    music_volume = clamp(music_volume + delta, 0.0, 1.0)
    save_data_manager.save(Data.music_volume, music_volume)


def change_sfx_volume(delta: float) -> None:
    """Increase or decrease the sound effect volume.

    Args:
        delta: the value by which to change the music volume
    """
    global sfx_volume
    sfx_volume = clamp(sfx_volume + delta, 0.0, 1.0)
    save_data_manager.save(Data.sfx_volume, sfx_volume)
