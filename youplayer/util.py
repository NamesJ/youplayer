import validators


def valid_youtube_url(url):
    if not validators.url(url):
        return False
    if not ('youtu.be' in url or 'youtube' in url):
        return False
    return True