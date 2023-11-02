#!/usr/bin/env python3


def find_sus(sets_dict: dict, set_key: str):
    s = sets_dict[set_key]
    other_sets_keys = list(sets_dict.keys())
    other_sets_keys.remove(set_key)
    for n in range(1, len(s) + 1):
        # Initialize a binary mask with the first n elements set to 1
        mask = (1 << n) - 1
        while mask < (1 << len(s)):
            subset = []
            # Iterate through the elements of the set and check if the corresponding
            # bit in the mask is set (1), if yes, add the element to the subset
            for i in range(len(s)):
                if (mask >> i) & 1:
                    subset.append(s[i])
            # check whether subset is sus
            sets_with_such_elements_number = 0
            for other_set_key in other_sets_keys:
                other_set = sets_dict[other_set_key]
                if all(e in other_set for e in subset):
                    sets_with_such_elements_number += 1
            if sets_with_such_elements_number == 0:
                return subset
            # Generate the next binary number with n 1s
            # This algorithm is known as Gosper's Hack
            c = mask & -mask
            r = mask + c
            mask = (((r ^ mask) >> 2) // c) | r
    return [""]


def naive_sus(sets_dict: dict):
    for set_key in sets_dict.keys():
        sus = find_sus(sets_dict, set_key)
        sus = "\t".join(sus)
        print(f"{set_key}\t{sus}")
