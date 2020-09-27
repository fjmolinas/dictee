#!/usr/bin/env python3

import argparse
import random
import pyttsx3
import time


DEFAULT_RATE = 125
DEFAULT_VOLUME = 1


parser = argparse.ArgumentParser(
        description='Read out a random series of Words')
parser.add_argument('words_file',
        help="File with list of words tu use as input")
parser.add_argument('--i','--interval', type=int, default=1, dest="interval",
        help='Interval to at which to read words [s]')
parser.add_argument('--n','--num', type=int, default=1, dest="num",
        help="Number of words to read")


def _get_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', DEFAULT_RATE)
    engine.setProperty('volume', DEFAULT_VOLUME)
    return engine


def _get_words_from_file(file_name):
    lines = []
    with open(file_name) as f:
        lines = f.read().splitlines()
    return lines


def main(args):
    eng = _get_engine()
    words = _get_words_from_file(args.words_file)
    num = args.num
    interval = args.interval
    if num > len(words):
        print("Error: not enough words in file {}".format(args.words_file))
        return
    idxs = random.sample(range(len(words)), num)
    
    print("Reading {} words every {} seconds".format(num, interval))
    for idx in idxs:
        word = words[idx]
        print("Saying word {}".format(word))
        eng.say(word)
        eng.runAndWait()
        if ifx < len(idxs):
            time.sleep(interval)


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    main(args)
