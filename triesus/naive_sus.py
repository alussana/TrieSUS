#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

def generate_subsets(s:list, n:int):
    def backtrack(start:int, current:list):
        if len(current) == n:
            subsets.append(current[:])
            return
        for i in range(start, len(s)):
            current.append(s[i])
            backtrack(i + 1, current)
            current.pop()
    subsets = []
    backtrack(0, [])
    return subsets

def find_sus(sets_dict:dict, set_key:str):
    elements_list = sets_dict[set_key]
    other_sets_keys = list(sets_dict.keys())
    other_sets_keys.remove(set_key)
    for subset_size_int in range(len(elements_list)):
        subsets = generate_subsets(elements_list, subset_size_int + 1)
        for subset in subsets:
            sets_with_such_elements_number = 0
            for other_set_key in other_sets_keys:
                other_set = sets_dict[other_set_key]
                if all(e in other_set for e in subset):
                    sets_with_such_elements_number += 1
            if sets_with_such_elements_number == 0:
                return subset
    return [""]
        
def naive_sus(sets_dict:dict):
    for set_key in sets_dict.keys():
        sus = find_sus(sets_dict, set_key)
        sus = '\t'.join(sus)
        print(f'{set_key}\t{sus}')