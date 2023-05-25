#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

def main():
    from triesus.run_triesus import run_triesus
    import sys
    run_triesus(sys.argv[1])
    
if __name__ == '__main__':
    main()