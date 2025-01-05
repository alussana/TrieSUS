#!/usr/bin/env python3

from triesus.input import *
from triesus.triesus import *


def run_triesus(collection_tsv: str, extended=False, output=None) -> None:
    collection_dict = read_collection(collection_tsv)

    triesus = TrieSUS(collection_dict)

    def print_solutions(out_fh=None):
        for key, item in triesus.collection.items():
            sus = triesus.find_sus(item, extended)
            if len(sus) > 0 and type(sus[0]) == list:
                for i in range(len(sus)):
                    optimal_sus = "\t".join(sus[i])
                    print(f"{key}\t{optimal_sus}", file=out_fh)
            else:
                sus = "\t".join(sus)
                print(f"{key}\t{sus}", file=out_fh)

    if output is None:
        print_solutions()
    else:
        with open(output, "w+") as output_fh:
            print_solutions(output_fh)
        print(f"  Output saved in {output}")
