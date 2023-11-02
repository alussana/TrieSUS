#!/usr/bin/env python3


class TrieNode:
    def __init__(self, parent=None, symbol=None):
        self.parent = parent
        self.children = {}
        self.is_end_of_word = False
        self.words_ending_here = 0
        self.symbol = symbol
