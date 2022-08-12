# NMNH-Coral-Lab

Feel free to use code for your own purposes, but please cite as according to the [citation file](CITATION.cff).

# Pipeline

### Purpose

This pipeline was created to take genome skim data of octocoral mtgenomes and reconstruct a phylogeny based on their gene orders. It does so as follows:

1. Trim the adapters from genome skim sequenced data using [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic).
2. Assemble and annotate the mtgenomes using [Mitofinder](https://github.com/RemiAllio/MitoFinder#submission-with-tbl2asn).
3. Extract gene orders from the assembled mtgenomes (specific to octocoral mtgenomes).
4. Construct a phylogeny from the assembled mtgenomes using [MAFFT](https://mafft.cbrc.jp/alignment/software/) and [IQ-TREE](http://www.iqtree.org).
5. Perform ancestral state reconstruction using [phytools](https://github.com/liamrevell/phytools).

### Dependencies

### Usage

#### 1. Trimming Adapters:

Use [trim_adapters.sh](trim_adapters.sh) by supplying the path to the reads (a directory holding files named things like "[sampleID]**R1**[other stuff]" for forward reads and "[sampleID]**R2**[other stuff]" for reverse reads), and the path to your adapters (a fasta file).
Be sure to change the path (and version) to trimmomatic if yours differs.

Example usage: 
```
bash trim_adapters.sh dir-with-reads adapters-fasta
```

#### 2. Assembling and Annotating the Mtgenomes

Use octo_mitofinder





















The project was funded under a NOAA OER grant to C. McFadden, A. Quattrini and S. Herrera.
Example files are provided for ease of use, these don't represent any actual findiings from this project


