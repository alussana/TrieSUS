#!/usr/bin/env python3

from triesus.input import *


def verify_unique_subset(items: list, collection: dict):
    sets_with_all_items = 0

    for key, item in collection.items():
        if all(e in item for e in items):
            sets_with_all_items += 1

    return sets_with_all_items == 1


def verify_all_unique_subsets(collection_us: dict, collection_all: dict):
    for key, item in collection_us.items():
        if verify_unique_subset(item, collection_all) == False:
            return False

    return True


if __name__ == "__main__":
    collection_dict = read_collection("tests/examples/test.tsv")
    subsets_dict = read_collection("subsets.tsv")

    print(verify_all_unique_subsets(subsets_dict, collection_dict))
