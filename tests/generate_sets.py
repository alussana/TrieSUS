#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

from triesus.random import *

def main():
    
    sets_dict = random_sets(200,200,300)
    
    print_sets(sets_dict)

if __name__ == '__main__':
    main()
    