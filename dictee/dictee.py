#!/usr/bin/env python3

import os
import sys
import argparse
import logging
import base64
import time
import glob
import random
from playsound import playsound

CURRENT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
DATA_DIR_DEFAULT = os.path.join(CURRENT_PATH, '../data')

LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'fatal', 'critical')

PARSER = argparse.ArgumentParser(
        description='Read out a random series of Words')
PARSER.add_argument('--words-dir', default=DATA_DIR_DEFAULT,
        help="Directory with words data")
PARSER.add_argument('--i','--interval', type=int, default=1, dest="interval",
        help='Interval to at which to read words [s]')
PARSER.add_argument('--n','--num', type=int, default=1, dest="num",
        help="Number of words to read")
PARSER.add_argument('--loglevel', choices=LOG_LEVELS, default='info',
                            help='Python logger log level')


def _get_words_in_dir(path):
    log = logging.getLogger("dictee")
    files = glob.glob("{}/*.wav".format(path))
    log.debug(files)
    words = []
    for file_path in files:
        word = os.path.basename(file_path).split('.')[0]
        log.debug(word)
        words.append(dict({word:file_path}))
    log.debug(words)
    return words

def main(args=None):
    args = PARSER.parse_args()
    log = logging.getLogger("dictee")
    if args.loglevel:
        loglevel = logging.getLevelName(args.loglevel.upper())
        log.setLevel(loglevel)

    log.addHandler(LOG_HANDLER)
    log.propagate = False

    words = _get_words_in_dir(args.words_dir)
    num = args.num
    interval = args.interval
    if num > len(words):
        log.error("Error: not enough words in file {}".format(args.words_dir))
        return
    idxs = random.sample(range(len(words)), num)
    
    log.info("Reading {} words every {} seconds".format(num, interval))
    for idx in idxs:
        d = words[idx]
        for word, path in d.items():
            log.info("Saying word {} in {}".format(word, path))
            playsound(path)
        if idx < len(idxs):
            time.sleep(interval)


if __name__ == "__main__":
    main()
