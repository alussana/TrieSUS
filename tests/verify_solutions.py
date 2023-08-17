
# Alessandro Lussana <alussana@ebi.ac.uk>

from triesus.input import *

def verify_unique_subset(

    items:list,
    collection:dict

):
    for key,item in collection:

        sets_with_all_items = 0

        if all(e in item for e in items):
                
                sets_with_all_items += 1

    return sets_with_all_items == 1

def verify_all_unique_subsets(
    
    collection_us:dict,
    collection_all:dict
    
):
    
    for key,item in collection_us:
    
        if verify_unique_subset(item, collection_all[key]) == False:
    
            return False
    
    return True