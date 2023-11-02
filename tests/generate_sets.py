#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

from triesus.random import *

if __name__ == "__main__":
    sets_dict = random_sets(18, 200, 206)

    print_sets(sets_dict)
