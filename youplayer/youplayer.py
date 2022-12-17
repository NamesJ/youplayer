from threading import Thread
import tkinter as tk
import os
from .musicplayer import BaseMusicPlayerApp
from .vlcplayer import VLCPlayer
from .ytdownloader import YTDownloaderApp, valid_url
from .telegrambot import TelegramBot


def start_app(app):
    app.mainloop()


class YouPlayer:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_path = None
        self.music_app = None
        self.download_app = None
        self.telegram_bot = None

    def start(self):
        self.music_app = VLCPlayer()
        self.music_app.vlc_init()
        self.download_app = YTDownloaderApp(
            on_downloaded=self.add_song,
            title='YouPlayer Song Downloader')
        self.download_path = self.download_app.save_path
        self.telegram_bot = TelegramBot(
            on_back=self.music_app.back,
            on_pause=self.music_app.pause,
            on_play=self.music_app.play,
            on_skip=self.music_app.skip,
            on_yt=self.add_download
        )
        self.telegram_bot.run()
        # NOTE: Add menubar option to music app to reopen download app
        if isinstance(self.music_app, VLCPlayer):
            self.download_app.mainloop()
        elif isinstance(self.music_app, BaseMusicPlayerApp):
            music_app_thread = Thread(target=self.music_mainloop)
            music_app_thread.start()
            self.download_app.mainloop()
            music_app_thread.join()

    def music_mainloop(self):
        self.music_app.mainloop()

    def download_mainloop(self):
        self.download_app.mainloop()

    def add_download(self, url: str):
        self.download_app.download(url)

    def set_download_path(self, path: str):
        self.download_path.set(path)

    def add_song(self, filename: str):
        path = f'{self.download_path.get()}/{filename}'
        if isinstance(self.music_app, VLCPlayer):
            self.music_app.add_song(path)
        elif isinstance(self.music_app, BaseMusicPlayerApp):
            self.music_app.add_song(path, path)


def main():
    yp = YouPlayer()
    yp.start()


if __name__ == '__main__':
    main()
