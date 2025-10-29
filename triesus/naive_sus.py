#!/usr/bin/env python3


def find_sus(sets_dict: dict, set_key: str, extended: bool = False):
    s = sets_dict[set_key]
    other_sets_keys = list(sets_dict.keys())
    other_sets_keys.remove(set_key)
    solutions = []
    min_n = 0
    for n in range(1, len(s) + 1):
        if min_n < n and len(solutions) > 0:
            return solutions
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
            is_sus = True
            for other_set_key in other_sets_keys:
                other_set = sets_dict[other_set_key]
                if all(e in other_set for e in subset):
                    is_sus = False
                    break
            if is_sus:
                if extended == False:
                    return subset
                else:
                    solutions.append(subset)
            # Generate the next binary number with n 1s (Gosper's Hack)
            c = mask & -mask
            r = mask + c
            mask = (((r ^ mask) >> 2) // c) | r
    return []


def naive_sus(sets_dict: dict, extended=False, output=None):

    def print_solutions(out_fh=None):
        for set_key in sets_dict.keys():
            sus = find_sus(sets_dict, set_key, extended)
            if len(sus) > 0 and type(sus[0]) == list:
                for i in range(len(sus)):
                    optimal_sus = "\t".join(sus[i])
                    print(f"{set_key}\t{optimal_sus}", file=out_fh)
            else:
                sus = "\t".join(sus)
                print(f"{set_key}\t{sus}", file=out_fh)

    if output is None:
        print_solutions()
    else:
        with open(output, "w+") as output_fh:
            print_solutions(output_fh)
        print(f"  Output saved in {output}")

