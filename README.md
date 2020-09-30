# WikiSearch
An Information Retrieval Project to extract the information from wiki dump and deploy search on it.

## Query Example

* 100, Sudebnik
* 10, t:Agostini ( t - title )

## Description

- This project generates a sorted indexer for the dump specified. It is optimized by compression techniques. Given a dump, it will create the inverted index file in Index/ folder, create a tree of indexers in Split/ folder for the inverted index and tree in Title/ for title-docID mappings file. Inverted index and title mapping file can be found in Index/ folder. 

- For a corpus of ~40GB , an index of ~14GB was created along with an mapping file of ~320MB.
- The index file was then split into smaller chunks in a B-tree manner so as to retrieve only the essential block instead of the whole file.


- Posting list contains the count of that term in title, body, infobox, references, external links and categories.

- T - Title
- B - body
- I - Infobox
- C - Categories
- L - External Links
- R - References
