import trrex as tx
import re

def main():
    pattern = tx.make(['122D', '125F'])
    # mt = pattern.match('345D')
    print(pattern)  # '\\b12(?:5F|2D)\\b'

if __name__ == '__main__':
    main()
