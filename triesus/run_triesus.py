#!/usr/bin/env python3

from triesus.input import *
from triesus.triesus import *


def run_triesus(collection_tsv: str) -> None:
    collection_dict = read_collection(collection_tsv)

    triesus = TrieSUS(collection_dict)

    for key, item in triesus.collection.items():
        sus = triesus.find_sus(item)
        sus = "\t".join(sus)
        print(f"{key}\t{sus}")
