import os
import shutil
import os.path
from pathlib import Path
from time import monotonic

import_dir = 'Z:/SRDS/DS-440/27'
export_dir = 'Z:/SRDS/DS-440/28'


def work():
    paths = sorted(Path(import_dir).iterdir(), key=os.path.getmtime)
    f = open(paths[0], "a")
    f.write("27\n")
    f.close()
    for root, subFolders, files in os.walk(import_dir):
        for file in files:
            subFolder = os.path.join(export_dir)
            shutil.move(os.path.join(root, file), subFolder)


t = monotonic()
while True:
    if monotonic() - t > 1:
        t = monotonic()
        if os.listdir(import_dir):
            work()
