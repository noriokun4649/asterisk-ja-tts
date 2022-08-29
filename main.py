#!/usr/bin/python3
import base64
import sys
from typing import Literal, TypedDict

import requests
from asterisk.agi import *


class OptionalKeys(TypedDict, total=False):
    format: Literal["wav", "mp3", "ogg"]
    emotion: Literal["happiness", "anger", "sadness"]
    emotion_level: int
    pitch: int
    speed: int
    volume: int


class RequiredKeys(TypedDict):
    text: str
    speaker: Literal["show", "haruka", "hikari", "takeru", "santa", "bear"]


class VoiceTextApiParams(RequiredKeys, OptionalKeys):
    pass


class VoiceTTS:
    def __init__(self):
        self.__hostname = "api.voicetext.jp"
        self.__endpoint = "v1/tts"
        self.__apikey = ""

    def getRequestUri(self):
        return f"https://{self.__hostname}/{self.__endpoint}"

    def getApiKey(self):
        return base64.b64encode(f"{self.__apikey}:".encode()).decode()

    def fetch(self, param: VoiceTextApiParams):
        return requests.post(
            self.getRequestUri(),
            data=param,
            headers={'Authorization': f'Basic {self.getApiKey()}'}
        ).content


if __name__ == "__main__":
    agi = AGI()
    message = sys.argv[1]
    tts = VoiceTTS()

    myParam: VoiceTextApiParams = {
        "text": message,
        "speaker": "show"
    }

    ret = tts.fetch(myParam)
    with open("filename.wav", "wb") as fout:
        fout.write(ret)

    agi.stream_file("filename", escape_digits='', sample_offset=0)
