from . import utilities as ut
import os
import yt_dlp

base_url = "http://www.youtube.com/watch?v="


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


def get_my_ydl(directory=os.path.dirname(os.path.abspath(__file__))):
    ydl = None
    outtmpl = None
    if ut.check_directory(directory):
        outtmpl = os.path.join(directory, "%(title)s.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": outtmpl,
            "logger": MyLogger(),
            "progress_hooks": [my_hook],
            "verbose": False,
            "ignoreerrors": "only_download",
            "external_downloader": "ffmpeg",
            "nocheckcertificate": True,
        }
        # 'external_downloader_args': "-j 8 -s 8 -x 8 -k 5M"}
        # 'maxBuffer': 'Infinity'}
        #  it uses multiple connections for speed up the downloading
        #  'external-downloader': 'ffmpeg'}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.cache.remove()
        import time

        time.sleep(0.5)
    return ydl


def audio_from_url(url, name, path_output, errors=[]):
    """
    Download audio from a url.
        url : str
            url of the video (after watch?v= in youtube)
        name : str
            used to store the data
        path_output : str
            path for storing the data
    """
    error = None

    # ydl(yt_dlp.YoutubeDL): extractor
    ydl = get_my_ydl(path_output)

    ydl.params["outtmpl"] = ydl.params["outtmpl"] % {
        "ext": ydl.params["postprocessors"][0]["preferredcodec"],
        "title": name,
    }

    if ydl:
        print("Downloading " + url)
        try:
            ydl.download([base_url + url])
        except Exception as e:
            print(e)
            error = e
    if error:
        errors.append([name, url, error])
    return


def audio_from_url_list(urls, path_output):
    """
    Download audio from a list of urls.
        urls : list
            urls of the videos (after watch?v= in youtube)
        path_output : str
            path for storing the data
    """
    ydl = get_my_ydl(path_output)
    ydl.params["outtmpl"]["ext"] = ydl.params["postprocessors"][0]["preferredcodec"]
    if ydl:
        try:
            ydl.download([base_url + url for url in urls])
        except Exception as e:
            print(e)
    return
