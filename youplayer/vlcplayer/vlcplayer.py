from threading import Thread
import vlc
import socket
import os
import subprocess
import sys


def run_vlc(vlc_path):
    subprocess.run(f'{vlc_path} --extraintf rc --rc-host 127.0.0.1:44500')


def __init():
    if os.name == 'nt':
        vlc_path = None
        vlc_64_path = os.path.abspath('C:\Program Files\VideoLAN\VLC')
        vlc_32_path = os.path.abspath(r'C:\Program Files (x86)\VideoLAN\VLC')

        if os.path.isdir(vlc_64_path):
            print('Adding VLC 64-bit')
            sys.path.append(vlc_64_path)
            vlc_path = os.path.join(vlc_64_path, 'vlc')
        elif os.path.isdir(vlc_32_path):
            print('Adding VLC 32-bit')
            sys.path.append(vlc_32_path)
            vlc_path = os.path.join(vlc_32_path, 'vlc')
        else:
            raise Exception('Unable to locate VLC installation')
    else:
        raise Exception('Non-windows systems not yet supported')
    Thread(target=run_vlc, args=(vlc_path,)).start()



class VLCPlayer:
    def __init__(self):
        self.is_initiated = False
        self.SEEK_TIME = 20
        self.MAX_VOL = 512
        self.MIN_VOL = 0
        self.DEFAULT_VOL = 256
        self.VOL_STEP = 13
        self.current_vol = self.DEFAULT_VOL

    def pause(self):
        if not self.is_initiated:
            self.vlc_init()
            return
        self.thrededreq('pause')

    def play(self):
        if not self.is_initiated:
            self.vlc_init()
            return
        self.thrededreq('play')

    def vlc_init(self):
        if not self.is_initiated:
            self.is_initiated = True
            self.thrededreq("loop on")
            return

    def add_song(self, path: str):
        if not self.is_initiated:
            self.vlc_init()
            return
        # Doesn't work with normal string path, so get absolute path via os pkg
        path = os.path.abspath(path)
        self.thrededreq(f'enqueue "{path}"')

    def skip(self):
        if not self.is_initiated:
            self.vlc_init()
            return
        self.thrededreq("next")
        print("Next")
        pass

    def back(self):
        if not self.is_initiated:
            self.vlc_init()
            return
        self.thrededreq("prev")
        print("Previous")
        pass

    def volup(self):
        self.current_vol = self.current_vol + self.VOL_STEP
        self.thrededreq("volume " + str(self.current_vol))
        print("Volume up")
        pass

    def voldown(self):
        self.current_vol = self.current_vol - self.VOL_STEP
        self.thrededreq("volume " + str(self.current_vol))
        print("Volume Down")
        pass

    def seek(self, forward: bool):
        length = self._timeinfo("get_length")
        print(length)
        cur = self._timeinfo("get_time")
        print(cur)
        if (forward):
            seekable = cur + self.SEEK_TIME
        else:
            seekable = cur - self.SEEK_TIME
        if seekable > length:
            seekable = length - 5
        if seekable < 0:
            seekable = 0
        self.thrededreq("seek " + str(seekable))
        print("Seek: ",seekable," Cur: ",cur,"Len: ",length)
        pass

    def _timeinfo(self, msg):
        length = self.req(msg, True).split("\r\n")
        if (len(length) < 2):
            return None
        length = length[1].split(" ")
        if (len(length) < 2):
            return None
        try:
            num = int(length[1])
            return num
        except:
            return None

    def req(self, msg: str, full=False):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data
                sock.settimeout(0.7)
                sock.connect(('127.0.0.1', 44500))
                response = ""
                received = ""
                sock.sendall(bytes(msg + '\n', "utf-8"))
                # if True:
                try:
                    while (True):
                        received = (sock.recv(1024)).decode()
                        response = response + received
                        if full:
                            b = response.count("\r\n")
                            if response.count("\r\n") > 1:
                                sock.close()
                                break
                        else:
                            if response.count("\r\n") > 0:
                                sock.close()
                                break
                except:
                    response = response + received
                    pass
                sock.close()
                return response
        except:
            return None
            pass

    def thrededreq(self, msg):
        Thread(target=self.req, args=(msg,)).start()


__init()


def main():
    #'vlc --intf rc --rc-host 127.0.0.1:44500' you need to run the vlc player from command line to allo controlling it via TCP
    player = VLCPlayer()
    player.toggle_play()
    #player.next()
    #player.prev()


if __name__ == '__main__':
    main()