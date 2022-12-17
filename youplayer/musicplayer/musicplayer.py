import tkinter as tk
from threading import Thread
import pygame
import pygame.mixer as mixer

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
mixer.init()

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)


class MusicPlayer:
    def __init__(self, song_title: tk.StringVar, songs: list,
                 status: tk.StringVar, on_ended=None):
        self.song_title = song_title
        self.songs = songs
        self.status = status
        self.status.set('INIT')
        self.on_ended = on_ended
        self.song_idx = 0
        self.song = None
        self.song_title.set('...')

    def check_music_end(self, root: tk.Frame):
        for event in pygame.event.get():
            if event.type != MUSIC_END:
                continue
            self.song_idx += 1
            if self.song_idx >= len(self.songs): # reached end
                self.stop()
                self.status.set('STOPPED')
                self.on_ended()
            if self.status.get() in {'INIT', 'STOPPED'}:
                self.song_title.set('')
            elif self.status.get() in {'PLAYING', 'PAUSED'}:
                self.song_title.set(self.songs[self.song_idx].title)
        root.after(500, self.check_music_end, root)

    def queue_all(self):
        mixer.music.stop()
        self.song_idx = 0
        mixer.music.load(self.songs[self.song_idx].path)
        for song in self.songs[self.song_idx:]:
            mixer.music.queue(song.path)
        self.song_title.set(self.songs[self.song_idx].title)

    def clear(self):
        self.song_idx = 0
        self.song = None
        self.songs = []
        self.stop()

    def load(self, songs):
        self.clear()
        self.songs = songs

    def add(self, song):
        self.songs.append(song)
        if self.status.get() in {'PAUSED', 'PLAYING'}:
            mixer.music.queue(song.path)

    def play(self):
        if len(self.songs) == 0:
            print('MusicPlayer.play(): No songs to play')
            return
        if self.status.get() == 'PAUSED':
            mixer.music.unpause()
        else:
            if self.song_idx < 0:
                self.song_idx = 0
            elif self.song_idx >= len(self.songs):
                self.song_idx %= len(self.songs)
            # Load songs up until end
            song = self.songs[self.song_idx]
            mixer.music.load(song.path)
            self.song_title.set(song.title)
            next_idx = (self.song_idx+1)%len(self.songs)
            if next_idx != self.song_idx:
                for song in self.songs[self.song_idx+1:]:
                    mixer.music.queue(song.path)
            mixer.music.play()
        self.status.set('PLAYING')

    def pause(self):
        mixer.music.pause()
        self.status.set('PAUSED')

    def resume(self):
        mixer.music.unpause()
        self.status.set('PLAYING')

    def stop(self):
        mixer.music.stop()
        self.song_idx = 0
        self.status.set('STOPPED')

    def back(self):
        self.song_idx -= 1
        self.status.set('BACK')
        self.play()

    def skip(self):
        self.song_idx += 1
        #self._update_song()
        self.status.set('SKIP')
        self.play()
