#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

from triesus.run_naive_sus import *

if __name__ == "__main__":
    print('tests/examples/sets1.tsv')
    run_naive_sus("tests/examples/sets1.tsv")
    print('tests/examples/sets2.tsv')
    run_naive_sus("tests/examples/sets2.tsv")
    print('tests/examples/sets3.tsv')
    run_naive_sus("tests/examples/sets3.tsv")
    print('tests/examples/6_6_6.tsv')
    run_naive_sus("tests/examples/6_6_6.tsv")