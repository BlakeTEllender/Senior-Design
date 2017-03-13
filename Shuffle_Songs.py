import random
import pygame

#This module shuffles songs
#songs must list of file paths when called
#and current_song must = None
def play_song(songs,current_song):
    next_song = random.choice(songs)
    while next_song == current_song:
        next_song = random.choice(songs)
    current_song = next_song
    return next_song

#This function plays and shuffles songs from a playlist when called
def music():
    song1 = '/home/pi/Downloads/The_Song_of_the_Butterfly_[Hungary_2014_HD.ogg'
    song2 = '/home/pi/Downloads/Rain and Native American Flute 2 - Shamanic Dream.ogg'
    song3 = '/home/pi/Downloads/Buddhist Meditation Music for Positive Energy Buddhist Thai Monks Chanting Healing Mantra.ogg'
    song4 = '/home/pi/Downloads/Kill Paris - Good Love.ogg'
    songs = [song1,song2,song3,song4]
    current_song = None
    song_End = pygame.USEREVENT + 1
    pygame.init()
    pygame.mixer.music.set_endevent(song_End)
    pygame.mixer.music.load(play_song(songs,current_song))
    pygame.mixer.music.play()
    #while True:
        #for event in pygame.event.get():
            #if event.type == song_End:
                #pygame.mixer.music.load(play_song(songs,current_song))
                #pygame.mixer.music.play()
