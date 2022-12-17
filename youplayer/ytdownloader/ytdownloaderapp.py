from typing import Callable
import tkinter
from threading import Thread
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkfont
from tkinter.constants import *
import os
from .util import download_audio, valid_url, get_filename, extract_audio

DEFAULT_NT_PATH = 'C:/Users/sande/Music/ytdownloads'


class DownloadInfo(ttk.Frame):
    def __init__(self, *args, url: str = None, filename: str = None,
                 status: tk.Variable = None,
                 font: tuple = None, relief: int = FLAT, **kwargs):
        super().__init__(*args, **kwargs)
        # tk vars
        self.url = tk.StringVar(value=url if url else '...')
        self.filename = tk.StringVar(value=filename if filename else '...')
        self.status = tk.StringVar(value=status if status else 'Downloading')

        # Entries for displaying info about download
        class InfoEntry(tk.Entry):
            def __init__(self, *ie_args, parent: tk.Frame = self,
                         state: str = DISABLED, font: tuple = font,
                         disabledforeground: str = 'black',
                         justify: int = CENTER, relief: int = relief,
                         **ie_kwargs):
                super().__init__(parent, *ie_args, state=state, font=font,
                                 disabledforeground=disabledforeground,
                                 justify=justify, relief=relief, **ie_kwargs)

            def pack(self, *ie_args, expand=True, fill=BOTH, **ie_kwargs):
                super().pack(*ie_args, expand=True, fill=fill, **ie_kwargs)

        InfoEntry(textvariable=self.url).pack(side=LEFT)
        InfoEntry(textvariable=self.filename).pack(side=LEFT)
        InfoEntry(textvariable=self.status).pack(side=RIGHT)


class LabelWidget(ttk.Label):
    def __init__(self, *args, font: tuple = ('Times New Roman', 14, 'bold'),
                 **kwargs):
        super().__init__(*args, font=font, **kwargs)


class YTDownloaderApp(tk.Tk):
    def __init__(self, *args, on_downloaded: Callable = None,
                 title: str = 'YouTube Song Downloader', **kwargs):
        super().__init__(*args, **kwargs)
        # Provided tk vars
        self.save_path = tk.StringVar(value='')
        self.save_path.set(DEFAULT_NT_PATH if os.name == 'nt' else '')
        # Callbacks
        self.on_downloaded = on_downloaded
        # Other tk vars
        self.url = tk.StringVar(value='')
        # Set geometry
        width, height = 700, 400
        screen_width = self.winfo_screenwidth()
        x = screen_width - width - 25  # right is 25 from screen right
        y = 80  # top is 80 from screen top
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.title(title)
        self.resizable(False, False)
        # Save path section
        path_frame = ttk.Labelframe(self, labelwidget=LabelWidget(
            self, text='Save path'))
        path_frame.pack(fill=X, side=TOP, padx=2, pady=4)
        ttk.Entry(path_frame, textvariable=self.save_path, state=DISABLED).pack(
            expand=True, side=LEFT, fill=BOTH)
        ttk.Button(path_frame, text='Change', command=self.set_path).pack(
            side=LEFT)
        # Add download section
        download_frame = ttk.Labelframe(self, labelwidget=ttk.Label(
            self, text='Add download'))
        download_frame.pack(fill=X, side=TOP, padx=2, pady=4)
        (ttk.Entry(download_frame, textvariable=self.url)
            .pack(expand=True, side=LEFT, fill=BOTH))
        self.download_btn = ttk.Button(download_frame, text='Download',
                                       command=self.download_clicked)
        # Disable button if initial save path is not valid
        if not os.path.isdir(self.save_path.get()):
            self.download_btn['state'] = DISABLED
        self.download_btn.pack(side=RIGHT, fill=Y)
        # Section to show URL and status of downloads
        self.info_frame = ttk.Labelframe(self, labelwidget=LabelWidget(
            self, text='Downloads'))
        self.info_frame.pack(expand=True, fill=BOTH, side=BOTTOM, padx=2,
                             pady=4)
        # Add headers to status frame
        DownloadInfo(self.info_frame, url='URL', filename='File Name',
                     status='Status', font=('Times New Roman', 12, 'bold'),
                     relief=FLAT)\
            .pack(expand=False, fill=X, side=TOP)
        # last_dl_info keeps track of last (top-most) DownloadInfo so that
        # next one can be packed before it to have most recent at top
        self.last_dl_info = None

        # One DownloadInfo frame will be added to info_frame for each download

    def set_path(self):
        path = filedialog.askdirectory(title='Save Directory')
        if not path:
            return
        self.save_path.set(path)
        self.download_btn['state'] = NORMAL

    def t_download(self, path: str, url: str):
        """
        Thread-safe download function
        :param path:
        :param url:
        :return:
        """
        info_frame = DownloadInfo(self.info_frame, url=url)
        info_frame.pack(before=self.last_dl_info, expand=False, fill=X,
                        side=TOP)
        self.last_dl_info = info_frame
        # Attempt to download audio and save to path
        #filename, title = download_audio(path, url)
        filename = get_filename(url)
        if filename:
            file_path = os.path.join(path, filename)
            extract_audio(file_path, url)
        status = 'Completed' if filename else 'Failed'
        info_frame.filename.set(filename)
        info_frame.status.set(status)
        # Call back if download successful
        if self.on_downloaded:
            self.on_downloaded(filename)

    def download(self, url: str):
        """
        Start a threaded download for the provided URL
        :param url:
        :return:
        """
        path = self.save_path.get()

        if not os.path.exists(path):
            messagebox.showerror('Path Error', 'Save path is invalid!')
            return
        if not valid_url(url):
            messagebox.showerror('URL Error', 'YouTube URL is invalid!')
            return

        Thread(target=self.t_download, args=(path, url), daemon=True).start()

    def download_clicked(self):
        """
        Start download. Called via UI
        :return:
        """
        url = self.url.get()
        self.url.set('')
        self.download(url)
