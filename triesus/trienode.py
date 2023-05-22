#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

class TrieNode:
    def __init__(self, parent=None, symbol=None):
        self.parent = parent
        self.children = {}
        self.is_end_of_word = False
        self.symbol = symbol