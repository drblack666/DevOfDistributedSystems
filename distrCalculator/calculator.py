import glob
import os
import os.path
from datetime import datetime
from pathlib import Path
from time import monotonic


def write_logs(operation_code, first_num, operations_count, operand):
    operations_dict = {
        0: "operation successfully done",
        1: "not mine operation",
        2: "file read"
    }
    with open(log_dir, 'a') as file:
        file.write(str(datetime.now()) + " " + str(operations_count) + " " + str(first_num) + " "
                   + operand + " " + operations_dict[operation_code] + "\n")


def work():
    paths = sorted(Path(import_dir).iterdir(), key=os.path.getmtime)
    with open(paths[0], 'r') as file:
        lines = file.readlines()

    num = lines[0].split('\n')[0]
    operand = lines[1].split(' ')[1].replace("\r", "").replace("\n", "")
    second_operand = lines[2].split(' ')[1].replace("\r", "").replace("\n", "")

    write_logs(2, num, len(lines), operand)

    if operand.startswith('^'):
        new_num = float(num) ** float(lines[1].split(' ')[0])
        lines[0] = str(new_num) + '\n'
        with open(os.path.join(export_dir, "new.txt"), 'w') as file:
            for line in lines:
                if line != lines[1]:
                    file.write(line)
        write_logs(0, new_num, len(lines) - 1, second_operand)
    else:
        with open(os.path.join(export_dir, "new.txt"), 'w') as file:
            for line in lines:
                file.write(line)
        write_logs(1, num, len(lines), operand)

    file_list = glob.glob(os.path.join(import_dir, "*.*"))
    for f in file_list:
        os.remove(f)


if __name__ == "__main__":
    import_dir = 'Z:/SRDS/DS-440/calc/group 2/5'
    export_dir = 'Z:/SRDS/DS-440/calc/group 2/6'
    log_dir = 'C:/Users/Shahovyuriia.Yu/Documents/log.txt'

    t = monotonic()
    while True:
        if monotonic() - t > 1:
            t = monotonic()
            for item in os.listdir(import_dir):
                if not item.startswith('.'):
                    work()
