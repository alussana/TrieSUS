#!/usr/bin/env python3


from triesus.trienode import *


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.end_nodes = []

    def insert(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                current.children[letter] = TrieNode(parent=current, symbol=letter)
            current = current.children[letter]
        current.is_end_of_word = True
        current.words_ending_here = current.words_ending_here + 1
        self.end_nodes.append(current)

    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return current.is_end_of_word

    def starts_with(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return True

    def end_node_for_word(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                return None
            current = current.children[letter]
        return current

    def prefix_from_node(self, node):
        prefix = []
        current = node
        while current.parent != None:
            prefix.append(current.parent)
            current = current.parent
        return prefix
