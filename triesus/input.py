#!/usr/bin/env python3


def read_collection(file_tsv: str) -> dict:
    with open(file_tsv) as file_fh:
        collection_dict = {}
        for line_str in file_fh:
            fields_list = line_str.strip().split("\t")
            set_id_str = fields_list.pop(0)
            collection_dict[set_id_str] = fields_list
    return collection_dict


def read_incidence_matrix(file_tsv: str) -> dict:
    with open(file_tsv) as file_fh:
        collection_dict = {}
        for line_str in file_fh:
            fields_list = line_str.strip().split("\t")
            set_id_str = fields_list.pop(0)
            collection_dict[set_id_str] = []
            for i in range(len(fields_list)):
                if int(fields_list[i]) == 1:
                    collection_dict[set_id_str].append(str(i))
    return collection_dict
