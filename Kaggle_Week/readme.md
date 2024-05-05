## Classes

Patings: The initial objects of input data

Frame glasses: The container of patings

LandscapeFG: The frame glass that contains landscape pating

ProtraitFG: The frame glass that contains protrait patings


## Objects

Maximize the final score

## Ideals

### Frame Glass Creation:

* Batch Processing: Patings are processed in batches to minimize memory usage and processing time.

* Type-Based Sorting: Patings are first categorized by type ('L' for landscape and 'P' for portrait).

* Tag-Based Pairing for Portraits: For portrait artworks, optimal pairs are selected based on the maximum difference in their tags

### Arrangement Algorithm:

* Greedy Method: Starting with the first frame glass, subsequent glasses are chosen based on a 'satisfaction' score calculated by a custom metric involving tag operations (union, intersection, difference).

* Sample Optimization: Random choose sample
