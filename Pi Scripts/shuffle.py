#This module shuffles songs
#songs must list of file paths when called
#and current_song must = None
import random

def play_song(songs,current_song):
    next_song = random.choice(songs)
    while next_song == current_song:
        next_song = random.choice(songs)
    current_song = next_song
    return next_song
    

