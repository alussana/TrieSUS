#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

from triesus.preprocessing import *
from triesus.triesus import *
    
def run_triesus(collection_tsv: str) -> None:
    collection_dict = read_collection(collection_tsv)
    item_counts_dict = item_counts(collection_dict)
    sorted_item_list = sort_keys_by_value(item_counts_dict)
    symbol_ranks = rank_dict_from_keys_list(sorted_item_list)
    collection_dict_sorted = sort_collection_by_other_list_order(collection_dict, sorted_item_list)
    triesus = TrieSUS(symbol_ranks)
    words = [item for key,item in collection_dict_sorted.items()]
    for word in words:
        triesus.insert(word)
    for key,item in collection_dict_sorted.items():
        sus = triesus.find_sus(item)
        sus = '\t'.join(sus)
        print(f'{key}\t{sus}')