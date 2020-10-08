#!/usr/bin/env python3

import sys
import os
import argparse
import json
import base64
import logging
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

SERVICE_URL = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com'
APP_KEY_FILE = open('.ibmappkey')
APP_KEY = base64.b64decode(APP_KEY_FILE.readline()).decode("utf-8")
VOICE_DEFAULT = 'fr-FR_ReneeVoice'

CURRENT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
OUTPUT_DIR = os.path.join(CURRENT_PATH, '../data')

LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'fatal', 'critical')

PARSER = argparse.ArgumentParser(
        description="Text to speech helper")
PARSER.add_argument('words', nargs='+',
                    help="list of words to store as audio files")
PARSER.add_argument('--voice', help="IBM TTS voice", default=VOICE_DEFAULT)
PARSER.add_argument('--output-dir', help="output directory", default=OUTPUT_DIR)
PARSER.add_argument('--loglevel', choices=LOG_LEVELS, default='info',
                            help='Python logger log level')


def _get_TTS():
    """Returns text to speech IBM service"""
    authenticator = IAMAuthenticator(APP_KEY)
    text_to_speech = TextToSpeechV1(authenticator=authenticator)
    text_to_speech.set_service_url(SERVICE_URL)
    return text_to_speech


def _synthethize_and_write(word, file_name, voice=VOICE_DEFAULT):
    """Synthethize 'word' and write to 'file_name.wav'"""
    tts = _get_TTS()
    with open(file_name, 'wb') as audio_file:
        audio_file.write(
                tts.synthesize(
                    word, voice=voice, accept='audio/wav'
                ).get_result().content)


def main(args=None): 
    """ Gets a list of french words and synthethizes it using IBM tts service"""
    args = PARSER.parse_args()
    log = logging.getLogger("tts")
    if args.loglevel:
        loglevel = logging.getLevelName(args.loglevel.upper())
        log.setLevel(loglevel)

    log.addHandler(LOG_HANDLER)
    log.propagate = False

    words = args.words
    voice = args.voice
    output_dir = args.output_dir

    # create output dir if it does not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    os.chdir(os.path.realpath(output_dir))

    for word in words:
        file_name = "{}.wav".format(word)
        log.debug("writing {} to {}".format(word, file_name))
        _synthethize_and_write(word=word, file_name=file_name)


if __name__ == "__main__":
    main()
