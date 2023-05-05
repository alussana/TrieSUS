# TrieSUS

## Find the Smallest Unique Subsets (SUS).

`TrieSUS` solves the following problem: given a collection of sets, map each set to the smallest possible combination of its elements that uniqly identifies the set

## Example

Consider the following collection of sets (the first field denotes the set id, the following fields are elements of the set. Fields are tab-separated):

```
1       C
2       A       B       D
3       B       E
4       A       D
```

The SUS for each set in this collection can be found running `./triesus.py examples/sets2.tsv`

```
1       C
2       D       B
3       E
4
```

Note that the smallest unique subset for set `4` does not exist.

## Algorithm

The algorithmic problem was discussed in this [StackOverflow question](https://stackoverflow.com/questions/63514798):

> *[...]*
> 
>  I have multiple sets with elements that are unique within each set, but may not be unique across all sets. How can I find the smallest possible subset of each set such that each subset is unique?
>
> *[...]*

A solution was proposed to find the SUS of a set `s` by first counting how many times each element in `s` appears in the other sets. It then sorts the elements in `s` based on this count, and considers all possible sub-arrays of `s`, returning the first one that satisfies the condition that it appears in exactly one set in the collection. If no such subset is found, the function returns `null`.
This procedure is repeated for every set in the collection.

`TrieSUS` adopts a different approach: it first ranks all the elements found in the sets of the collection from the most frequent to the least frequent. Then, it sorts the elements in the sets according to these ranks. Each set is then treated as a sorted list to build a prefix tree. Finally, for each set an efficient procedure that uses the prefix tree is followed to 1) determine whether a SUS exists, and 2) if appropriate, return a SUS.

The same problem also appears in this other [StackExchange question](https://math.stackexchange.com/questions/2436161), where no answer was given at the time of writing.

### Pseudocode

```
[...]
```

## Limitations

When multiple SUSs exist for a set, only the solution containing elements occurring with the lowest frequency in the collection is reported