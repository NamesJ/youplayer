import tkinter as tk
from tkinter import ttk, font
from tkinter.constants import *
from ..musicplayer import MusicPlayer
from ..song import Song


class Emoji:
    back = '⏮️' or '⏮'
    play = '▶️' or '▶'
    pause = '⏸️' or '⏸'
    play_or_pause = '⏯️' or '⏯'
    skip = '⏭️' or '⏭'
    stop = '⏹️' or '⏹'
    shuffle = '🔀'
    repeat = '🔁'
    repeat_single = '🔂'


class ControlButton(tk.Button):
    def pack(self, *args, ipadx: int = 10, ipady: int = 10, padx: int = 2,
             **kwargs):
        super().pack(*args, ipadx=ipadx, ipady=ipady, padx=padx, **kwargs)


class BaseMusicPlayerApp(tk.Tk):
    def __init__(self, *args, do_loop: bool = True, title: str = 'Music Player',
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.do_loop = do_loop

        width, height = 700, 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width - width - 25  # right is 25 from screen right
        y = screen_height - height - 80  # bottom is 80 from screen bottom
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.title(title)
        self.resizable(False, False)

        # Tkinter vars
        song_title = tk.StringVar()
        self.status = tk.StringVar()
        self.titles = tk.Variable(value=[])

        playing_frame = ttk.Labelframe(self, text='Currently playing')
        playing_frame.pack(fill=X, side=TOP, padx=2, pady=4)
        self.playing = ttk.Label(playing_frame, textvariable=song_title)
        self.playing.pack(expand=True, fill=BOTH)

        # will contain list of all songs
        playlist_frame = ttk.Labelframe(self, text='Playlist')
        playlist_frame.pack(expand=True, fill=BOTH, side=TOP)
        self.playlist = tk.Listbox(playlist_frame, listvariable=self.titles)
        self.playlist.pack(expand=True, fill=BOTH, side=TOP)

        controls = ttk.Frame(self)
        controls.pack(side=BOTTOM, padx=2, pady=4)

        control_btn_font = tk.font.Font(self, family='Times New Roman', size=18,
                                        weight='bold')
        back_btn = ControlButton(controls, text=Emoji.back, command=self.back)
        back_btn['font'] = control_btn_font
        back_btn.pack(side=LEFT)
        play_pause = ttk.Frame(controls)
        play_pause.pack(side=LEFT)
        self.play_btn = ControlButton(play_pause, text=Emoji.play,
                                      command=self.play)
        self.play_btn['font'] = control_btn_font
        self.play_btn.pack(side=LEFT)
        self.pause_btn = ControlButton(play_pause, text=Emoji.pause,
                                       command=self.pause)
        self.pause_btn['font'] = control_btn_font
        self.pause_btn.pack(side=LEFT)
        self.pause_btn.pack_forget()
        skip_btn = ControlButton(controls, text=Emoji.skip, command=self.skip)
        skip_btn['font'] = control_btn_font
        skip_btn.pack(side=LEFT)

        self.music_player = MusicPlayer(song_title, [], self.status,
                                        on_ended=self.on_ended)
        self.music_player.check_music_end(self)

    def on_ended(self):
        if self.do_loop:
            self.music_player.play()
        else:
            self.pause_btn.pack_forget()
            self.play_btn.pack(side=LEFT, fill=BOTH)

    def clear_songs(self):
        self.titles.set([])
        self.music_player.clear()

    def load_songs(self, tracks: list[tuple]):
        songs = []
        titles = []
        for path, title in tracks:
            songs.append(Song(path, title))
            titles.append(title)
        self.titles.set(titles)
        self.music_player.load(songs)

    def add_song(self, path: str, title: str):
        song = Song(path, title)
        titles = self.titles.get()
        if isinstance(titles, str):
            titles = []
        titles = list(titles)
        titles.append(song.title)
        self.titles.set(titles)
        self.music_player.add(song)

    def back(self):
        self.music_player.back()

    def play(self):
        if not len(self.music_player.songs):
            return
        if self.status.get() == 'PLAYING':
            return
        if self.status.get() in {'INIT', 'STOPPED'}:
            self.music_player.play()
        elif self.status.get() == 'PAUSED':
            self.music_player.resume()
        self.play_btn.pack_forget()
        self.pause_btn.pack(side=LEFT, fill=BOTH)

    def pause(self):
        if self.status.get() in {'INIT', 'STOPPED', 'PAUSED'}:
            return
        self.music_player.pause()
        self.pause_btn.pack_forget()
        self.play_btn.pack(side=LEFT, fill=BOTH)

    def skip(self):
        self.music_player.skip()


def main():
    app = BaseMusicPlayerApp()
    app.mainloop()


if __name__ == '__main__':
    main()
