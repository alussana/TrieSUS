#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

from triesus.input import *
from triesus.naive_sus import *
        
def run_naive_sus(collection_tsv: str):
    
    collection_dict = read_collection(collection_tsv)
    
    naive_sus(collection_dict)
    