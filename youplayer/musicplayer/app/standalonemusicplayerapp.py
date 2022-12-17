import tkinter as tk
from tkinter import filedialog
import os
from .basemusicplayerapp import BaseMusicPlayerApp
from ..song import Song


class StandaloneMusicPlayerApp(BaseMusicPlayerApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menubar = tk.Menu(self)
        menubar.add_command(label='Import', command=self.import_songs)
        self.config(menu=menubar)

    def import_songs(self):
        tracks_dir = filedialog.askdirectory(title='Open a songs directory')
        tracks = []
        for filename in os.listdir(tracks_dir):
            # Using file basename as title
            title, ext = os.path.splitext(filename)
            if ext.lower() not in {'.opus', '.ogg', '.wav'}:
                continue
            path = os.path.join(tracks_dir, filename)
            tracks.append((path, title))
        self.load_songs(tracks)


def main():
    app = StandaloneMusicPlayerApp()
    app.mainloop()


if __name__ == '__main__':
    main()