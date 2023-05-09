# TrieSUS

## Find the Smallest Unique Subset (SUS)

Given a collection of sets, `TrieSUS` maps each set to the smallest possible combination of its elements that uniquely identifies the set.

## Example

Consider the following collection of sets (the first field denotes the set id, the following fields are elements of the set. Fields are tab-separated):

```
1       C
2       A       B       D
3       B       E
4       A       D
```

The Smallest Unique Subset (SUS) for each set in this collection can be found running `./triesus.py examples/sets2.tsv`

```
1       C
2       D       B
3       E
4
```

Note that the SUS for set `4` does not exist.

## Algorithm

The algorithmic problem was discussed in this [StackOverflow question](https://stackoverflow.com/questions/63514798):

> *[...]*
> 
>  I have multiple sets with elements that are unique within each set, but may not be unique across all sets. How can I find the smallest possible subset of each set such that each subset is unique?
>
> *[...]*

A solution was proposed to find the SUS of a set `s` by first counting how many times each element in `s` appears in the other sets. It then sorts the elements in `s` based on this count, and considers all possible sub-arrays of `s`, returning the first one that satisfies the condition that it appears in exactly one set in the collection. If no such subset is found, the function returns `null`.
This procedure is repeated for every set in the collection.

`TrieSUS` adopts a different approach: it first ranks all the elements found in the sets of the collection from the most frequent to the least frequent. Then, it sorts the elements in the sets according to those ranks. Each set is then treated as a sorted list to build a prefix tree. Finally, for each set an efficient procedure (see [Pseudocode](#pseudocode)) that uses the prefix tree is followed to 1) determine whether a SUS exists, and 2) if appropriate, return a SUS.

The same problem also appears in this other [StackExchange question](https://math.stackexchange.com/questions/2436161), where no answer was given at the time of writing.

### Pseudocode

The function that returns a SUS is described below, and it corresponds to `Trie.find_sus()` in the codebase. It is assumed that the following relevant functions or data structures exist: 

* `word`: list of strings. The items (symbols) of the set for which we want to find the smallest unique subset.
* `symbol_ranks`: dictionary mapping each key to its corresponding rank. The item (symbol) occurring most frequently in the sets of the collection is given rank `1`.
* `trie`: a prefix tree
  * `end_nodes`: attribute of `trie`. List of nodes that mark the end of the words in the prefix tree.
  * Each node in `trie` has the following attributes:
    * `symbol`: a string. An item found in the the collection of sets
    * `parent`: the parent node of the node in the prefix tree
* `end_node_for_word`: function that takes in input a `word` and a `trie`, and returns the node that marks the end of that word in the prefix tree.

```{bash}
FUNCTION find_sus(word, trie)
    sus = []                                                          # Initialize empty list to store SUS
    word_end_node = end_node_for_word(word)                           # Get the node marking the end of the given word
    other_end_nodes = []                                              # Get a list of nodes marking the end of the other words
    FOR node IN trie.end_nodes                                        #   .
        IF node != word_end_node                                      #   .
            APPEND node TO other_end_nodes                            #   .
    IF length of word_end_node.children != 0                          # If word_end_node has children, then we know that the SUS doesn't exist
        RETURN []                                                     #   .
    APPEND word_end_node.symbol TO sus                                # The item with the greatest rank in the set will be in the SUS
    FOR end_node IN other_end_nodes                                   # Visit each other word
        current_word_node = word_end_node                             # Set pointers to the current
        current_trie_node = end_node                                  #   nodes being compared
        WHILE symbol_ranks[current_trie_node.symbol] >= symbol_ranks[current_word_node.symbol]  # Visit and compare further only if the rank of current_trie_node.symbol is >= the rank of current_word_node.symbol. Otherwise, visit the next word
            IF current_trie_node.symbol == current_word_node.symbol   # If the symbols are the same
                IF current_word_node.parent.parent == None            # If current_word_node's parent is the root of the trie
                    RETURN []                                         #   then the SUS doesn't exist
                ELSE                                                  # Otherwise extend the tentative SUS and visit the parent nodes
                    current_word_node = current_word_node.parent      # Move up in the word branch
                    IF current_word_node.symbol NOT IN sus            # If the item is not already in the SUS
                        APPEND current_word_node.symbol TO sus        #   then add the symbol to the SUS
            IF current_trie_node.parent.parent != None                # If current_trie_node's parent's is not the root
                current_trie_node = current_trie_node.parent          #   Then move up to the parent node
            ELSE                                                      # Otherwise there are no more items left to check in the current word
                BREAK                                                 # Exit the while loop
    RETURN sus                                                        # Return the SUS
```

## Limitations

When multiple SUSs exist for a set, only the solution containing elements occurring with the lowest frequency in the collection is reported.