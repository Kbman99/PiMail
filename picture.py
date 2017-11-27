from subprocess import call
from datetime import datetime
from config import dir
import os

# TODO: https://elinux.org/RPi_USB_Webcams
def capture(picture_count):
    path_list = []
    for i in range(picture_count):
        file_count = num_files('./FrameCap')
        dt = datetime.now()
        dtime = datetime.strftime(dt, "%b %d %Y %H:%M:%S")
        path = "./{}/{}.jpg".format(dir, dtime)
        # Simple check to ensure camera takes picture due to odd bug
        while num_files('./FrameCap') == file_count:
            call(["fswebcam", "-d","/dev/video0", "-r", "1280x720", "--no-banner", "./{}/{}.jpg".format(dir, dtime)])
        path_list.append(path)
    return path_list
    
    
def num_files(dir):
    list = os.listdir(dir) # dir is your directory path
    return len(list)

