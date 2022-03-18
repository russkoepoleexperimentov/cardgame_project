from datetime import datetime

LOG_FILE_NAME = 'log.txt'
LOG_LINE_WIDTH = 40
log = []


def trace(string: str):
    t = f'[{str(datetime.now())}] {string}'
    print(t)
    log.append(t)
    log.append('\n')


def add_line():
    t = '-' * LOG_LINE_WIDTH
    print(t)
    log.append(t)
    log.append('\n')


def start():
    log.append('\n\n')
    add_line()
    trace('log started!')


def end():
    trace('log finished!')
    add_line()
    file_stream = open(LOG_FILE_NAME, 'a')
    for line in log:
        file_stream.write(line)
    file_stream.close()
