# WikiSearch
An Information Retrieval Project to extract the information from wiki dump and deploy search on it.

## Query Example

* 100, Sudebnik
* 10, t:Agostini ( t - title )

## Description

-This project generates a sorted indexer for the dump specified. It is optimized by compression techniques. Given a dump, it will create the inverted index file in Index/ folder, create a tree of indexers in Split/ folder for the inverted index and tree in Title/ for title-docID mappings file. Inverted index and title mapping file can be found in Index/ folder. 

- Posting list contains the count of that term in title, body, infobox, references, external links and categories.

- T - Title
- X - body
- I - Infobox
- C - Categories
- L - External Links
- R - References
