import glob
import os
import os.path
from datetime import datetime
from pathlib import Path
from time import monotonic


def work():
    paths = sorted(Path(import_dir).iterdir(), key=os.path.getmtime)
    with open(paths[0], 'r') as file:
        lines = file.readlines()

    num = lines[0].split('\n')[0]
    operand = lines[1].split(' ')[1].replace("\r", "").replace("\n", "")

    with open(log_dir, 'a') as file:
        file.write(str(datetime.now()) + " " + str(len(lines)) + " " + num + " " + operand + "\n")

    if operand.startswith('^'):
        new_num = float(num) ** float(lines[1].split(' ')[0])
        lines[0] = str(new_num) + '\n'
        with open(os.path.join(export_dir, "new.txt"), 'w') as file:
            for line in lines:
                if line != lines[1]:
                    file.write(line)
        with open(log_dir, 'a') as file:
            file.write(str(datetime.now()) + " " + str(len(lines) - 1) + " " + str(new_num) + " "
                       + lines[2].split(' ')[1].replace("\r", "").replace("\n", "") + " operation successfully done\n")
    else:
        with open(log_dir, 'a') as file:
            file.write(str(datetime.now()) + " " + str(len(lines)) + " " + num + " "
                       + operand + " not mine operation\n")

    file_list = glob.glob(os.path.join(import_dir, "*.*"))
    for f in file_list:
        os.remove(f)


if __name__ == "__main__":
    import_dir = 'Z:/SRDS/DS-440/calc/group2/5'
    export_dir = 'Z:/SRDS/DS-440/calc/group2/6s'
    log_dir = 'C:/Users/Shahovyuriia.Yu/Documents/log.txt'

    t = monotonic()
    while True:
        if monotonic() - t > 1:
            t = monotonic()
            for item in os.listdir(import_dir):
                if not item.startswith('.'):
                    work()
