#!/usr/bin/env python3

from udpipe2_client import process

import requests

import sys


def udpipe(data: str) -> str:
    class ag:
        def __init__(self) -> None:
            self.inputs = []
            self.list_models = False
            self.input = "horizontal"
            self.model = None
            # self.model = 'english-ewt-ud-2.15-241121'
            self.output = "conllu"
            self.parser = "yes"
            self.tagger = "yes"
            self.tokenizer = "yes"
            self.outfile = None
            self.service = "https://lindat.mff.cuni.cz/services/udpipe/api"

    return process(
        args=ag(),
        data=data,
    )


def nametag(data: str) -> str:
    query = {
        "data": data,
        "input": "conllu",
        "output": "conllu-ne",
        "model": "nametag3-czech-cnec2.0-240830",
    }
    # query = {'data': data, 'input': 'conllu', 'output': 'conllu-ne', 'model': 'nametag3-multilingual-conll-240830'}
    response = requests.post(
        "https://lindat.mff.cuni.cz/services/nametag/api/recognize", data=query
    )
    return response.json()["result"]


def parse(data: str) -> str:
    return nametag(udpipe(data))


def main():
    print(parse(" ".join(sys.stdin.readlines())))


if __name__ == "__main__":
    main()
