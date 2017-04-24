#This function plays and shuffles songs from a playlist when called
def music():
    import pygame
    from shuffle import play_song
    song1 = '/home/pi/Downloads/The_Song_of_the_Butterfly_[Hungary_2014_HD.ogg'
    song2 = '/home/pi/Downloads/Rain and Native American Flute 2 - Shamanic Dream.ogg'
    song3 = '/home/pi/Downloads/Buddhist Meditation Music for Positive Energy Buddhist Thai Monks Chanting Healing Mantra.ogg'
    songs = [song1,song2,song3]
    current_song = None
    pygame.mixer.init()
    pygame.mixer.music.load(play_song(songs,current_song))
    pygame.mixer.music.play()
