#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

def read_collection(file_tsv:str) -> dict:
    with open(file_tsv) as file_fh:
        collection_dict = {}
        for line_str in file_fh:
            fields_list = line_str.strip().split('\t')
            set_id_str = fields_list.pop(0)
            collection_dict[set_id_str] = fields_list
    return collection_dict
            
def item_counts(collection_dict: dict) -> dict:
    item_list = []
    for key,item in collection_dict.items():
        item_list = item_list + item
    item_count_dict = {}
    for item_str in item_list:
        if item_str in item_count_dict:
            item_count_dict[item_str] += 1
        else:
            item_count_dict[item_str] = 1
    return item_count_dict

def sort_keys_by_value(dict_obj: dict) -> list:
    items = list(dict_obj.items())
    items.sort(key=lambda x: x[1], reverse=True)
    sorted_keys = [item[0] for item in items]
    return sorted_keys

def rank_dict_from_keys_list(keys_list: list):
    rank_dict = {}
    for i, key in enumerate(keys_list):
        rank_dict[key] = i + 1
    return rank_dict

def sort_list_by_other_list_order(my_list: list, other_list: list) -> list:
    item_to_index = {item: other_list.index(item) for item in my_list if item in other_list}
    sorted_list = sorted(my_list, key=lambda x: item_to_index.get(x, len(other_list)))
    return sorted_list

def sort_collection_by_other_list_order(collection_dict: dict, sorted_items_list: list) -> dict:
    for key in collection_dict.keys():
        collection_dict[key] = sort_list_by_other_list_order(collection_dict[key], sorted_items_list)
    return collection_dict