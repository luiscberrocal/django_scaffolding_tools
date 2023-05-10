from time import sleep

LINE_CLEAR = '\x1b[2k'
LINE_UP = '\033[1A'


def print_single():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for idx in range(len(characters) + 1):
        print(characters[:idx], end='\r')
        sleep(0.25)
    print(LINE_CLEAR)
    print('Finished')


def print_single2():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for idx in range(len(characters) + 1):
        print(characters[:idx], end='\r')
        sleep(0.25)
    print(LINE_UP, end=LINE_CLEAR)



if __name__ == '__main__':
    print_single2()
