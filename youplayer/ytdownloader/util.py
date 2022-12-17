import os

import yt_dlp
from filename_sanitizer import sanitize_path_fragment


def get_filename(url: str, codec: str = 'wav'):
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info = ydl.sanitize_info(info)
    except:
        print('Failed to extract info')
        return None
    title = info['title']
    filename = '{title} [{id}].{ext}'.format(
        title=title,
        id=info['id'],
        ext=codec
    )
    filename = sanitize_path_fragment(
        filename,
        target_file_systems={'ntfs_win32'},
        replacement=u'-')
    return filename


def extract_audio(path: str, url: str):
    codec = os.path.splitext(path)[1]
    ydl_opts = {
        'format': f'{codec}/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec
        }],
        'outtmpl': {
            'default': path
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)
            if error_code:
                raise Exception()
    except Exception:
        print('Failed to download')
        return False

    return True


def download_audio(dl_dir, url, codec='wav'):
    ydl_opts = {
        'format': f'{codec}/bestaudio/best',
        'postprocessors': [{ # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info = ydl.sanitize_info(info)
    except:
        print('Failed to extract info')
        return None, None

    title = info['title']
    filename = '{title} [{id}].{ext}'.format(
        title=title,
        id=info['id'],
        ext=codec
    )
    filename = sanitize_path_fragment(
        filename,
        target_file_systems={'ntfs_win32'},
        replacement=u'-')
    # Add out template option as sanitized filename
    ydl_opts['outtmpl'] = {
        'default': f'{dl_dir}/{filename}'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)
            if error_code:
                raise Exception()
    except Exception:
        print('Failed to download')
        return None, None

    return filename, title
