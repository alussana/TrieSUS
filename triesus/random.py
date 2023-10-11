#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

from random import choice

def random_sets(
    
    n:int,
    m:int,
    e:int

) -> dict:
    
    x = {}
    
    keys = [i for i in range(n)]
    
    elements = [str(i) for i in range(e)]
    
    for i in range(n):
    
        x[i] = [choice(elements) for j in range(m)]
        x[i] = set(x[i])
        x[i] = list(x[i])
    
    return x        

def print_sets(
    
    x:dict

) -> None:

    for key,item in x.items():
        row = str(key) + '\t' + '\t'.join(item)
        print(row)

def main():
    sets_dict = random_sets(100,100,200)
    print_sets(sets_dict)

if __name__ == '__main__':
    main()
    