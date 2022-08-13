# NMNH-Coral-Lab

Feel free to use code for your own purposes, but please cite as according to the [citation file](CITATION.cff).

# Pipeline

### Purpose

This pipeline was created to take genome skim data of octocoral mitogenomes and reconstruct a phylogeny based on their gene orders. It does so as follows:

1. Trim the adapters from genome skim sequenced data using [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic).
2. Assemble and annotate the mitogenomes using [Mitofinder](https://github.com/RemiAllio/MitoFinder#submission-with-tbl2asn).
3. Extract gene orders from the assembled mitogenomes (specific to octocoral mtgenomes).
4. Construct a phylogeny from the assembled mitogenomes using [MAFFT](https://mafft.cbrc.jp/alignment/software/) and [IQ-TREE](http://www.iqtree.org).
5. Perform ancestral state reconstruction using [phytools](https://github.com/liamrevell/phytools).

### Usage

### 1. Trimming Adapters:
Dependency: [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)


#### [trim_adapters.sh](trim_adapters.sh)
Use [trim_adapters.sh](trim_adapters.sh) by supplying the path to the reads (a directory holding files named things like "[sampleID]**R1**[other stuff]" for forward reads and "[sampleID]**R2**[other stuff]" for reverse reads), and the path to your adapters (a fasta file).
Be sure to change the path (and version) to trimmomatic if yours differs.

Example usage: 
```
bash trim_adapters.sh dir-with-reads adapters-fasta
```

### 2. Assembling and Annotating the Mitogenomes
Dependency: [Mitofinder](https://github.com/RemiAllio/MitoFinder#submission-with-tbl2asn)


#### [octo_mitofinder.sh](octo_mitofinder.sh)
Use [octo_mitofinder.sh](octo_mitofinder.sh) by supplying the path to the reads (a directory holding files named things like "[sampleID]**R1**[other stuff]" for forward reads and "[sampleID]**R2**[other stuff]" for reverse reads), and the path to your seed database (a .gb file holding whatever octocoral mtgenomes you want to use).
Be sure to change the path (and version) to mitofinder if yours differs.

Example usage:
```
bash octo_mitofinder.sh dir-with-reads database.gb
```

### 3. Extract Gene Orders from Octocoral Mitogenomes
Dependencies: [Biopython](https://biopython.org), and optionally the webserver at [here](http://trna.ucsc.edu/tRNAscan-SE/).

#### [gene_order_script.sh](gene_order_script.sh)
Recommended: If you'd like to make your life easier, first use [gene_order_script.sh](gene_order_script.sh) to aggregate all the .gb and .infos files you need from the mitofinder results into a new directory.

Example usage:
```
bash gene_order_script.sh dir-with-mitofinder-results
```

#### [gene_order.py](gene_order.py)
Use [gene_order.py](gene_order.py) by supplying the path to a directory of .gb files you want to extract the gene orders from (also accepts the name of a single .gb file). You can also specify the name of your output file with --name, and whether or not to overwrite pre-existing files with --overwrite.

This will output a csv with a gene order match for every sample as well as information from their .infos file such as mitogenome length, GC content, and circularization. It grabs gene orders from [gene_order_params.py](gene_order_params.py) (more on that later).

Example usage:
```
python gene_order.py dir-with-gb-files --name output-name --overwrite
```

#### [gene_order_params.py](gene_order_params.py)
You can (and probably should) edit [gene_order_params.py](gene_order_params.py) to fit your preferences. It includes the 8 octogenomes I was interested in for this project, but you may wish to rename them or add your own. When adding new gene orders, make sure to add them as a tuple with gene names matching those of the other gene orders. 

For instance, here are a few valid gene orders.
```
class GeneOrder(Enum):
    A =     ('cox1', 'rrns', 'nad1', 'cob', 'nad6', 'nad3', 'nad4l', 'muts', 'rrnl', 'nad2', 'nad5', 'nad4', 'trnm', 'cox3', 'atp6', 'atp8', 'cox2')
    B =     ('cox1', 'rrns', 'nad1', 'cob', 'cox3', 'trnm', 'nad4', 'nad5', 'nad2', 'rrnl', 'muts', 'nad4l', 'nad3', 'nad6', 'atp6', 'atp8', 'cox2')
    C =     ('cox1', 'rrns', 'nad1', 'cob', 'cox2', 'atp8', 'atp6', 'cox3', 'trnm', 'nad4', 'nad5', 'nad2', 'rrnl', 'muts', 'nad4l', 'nad3', 'nad6')
```

You should also edit the expected_genes variable in this file, which deals with certain genes having multiple names. This variable is a tuple of tuples, where each 2nd order tuple contains every possible name for a gene, where the first name for a gene matches the one displayed in the gene orders. The expected genes should already include all names that mitofinder will use, but if you use a seperate annotating process, yours may differ.

For instance, here is what it should look like:
```
expected_genes = (('cox1',), ('rrns','rns'), ('nad1','nd1'), ('cob','cytb'), ('nad6','nd6'), ('nad3','nd3'), ('nad4l','nd4l'), ('muts',), ('rrnl','rnl'), ('nad2','nd2'), ('nad5','nd5'), ('nad4','nd4'), ('trnm','trna-met'), ('cox3',), ('atp6',), ('atp8',), ('cox2',))
```
So, the gene 'rns' will be forced to be named 'rrns' in order to match the gene order Enums, and 'nd6' becomes 'nad6'.

If you also wish, you can change the start gene in the parameters file. cox1 is widely used as the start for gene orders, but if you wish to have a different start be sure to change the gene order Enums to match.


#### [tRNAscan-SE](https://github.com/UCSC-LoweLab/tRNAscan-SE)
Recommended: Note that mitofinder likes to annotate tRNAs that don't actually exist in octocoral mitogenomes. You will likely see a number of faulty tRNAs detected by [gene_order.py](gene_order.py). If you would like to verify that these are in fact faulty, use [tRNAscan-SE](https://github.com/UCSC-LoweLab/tRNAscan-SE) to double check your mitogenome files. They have a webserver [here](http://trna.ucsc.edu/tRNAscan-SE/) which accepts a fasta file, just remember to set the source to invertebrate mitochondrial.

### 4. Construct Phylogeny from Mitofinder Results
Dependencies: [MAFFT](https://mafft.cbrc.jp/alignment/software/) and [IQ-TREE](http://www.iqtree.org). Feel free to use their webservers rather than running them manually. Also optionally [ape](https://cran.r-project.org/web/packages/ape/index.html) and [phytools](https://github.com/liamrevell/phytools).

#### [alignment_script.sh](alignment_script.sh)
Recommended: If you'd like to make your life easier, first use [alignment_script.sh](alignment_script.sh) to aggregate all the .fasta files you need from the mitofinder results into a new directory.

Example usage:
```
bash alignment_script.sh dir-with-mitofinder-results
```

#### [alignment_from_mitofinder.py](alignment_from_mitofinder.py)
Use [alignment_from_mitofinder.py](alignment_from_mitofinder.py) by supplying the path to a directory of .fasta files you want to create alignment files for. It will create a fasta file for each gene found (so, every gene in the mitochondrial genomes) ready for alignment. You can specify whether or not to overwrite pre-existing files with --overwrite.

Example usage:
```
python alignment_from_mitofinder.py dir-with-fasta-files --overwrite
```

#### [MAFFT](https://mafft.cbrc.jp/alignment/software/)

I use [MAFFT](https://mafft.cbrc.jp/alignment/software/) locally, but you can use their webserver [here](https://mafft.cbrc.jp/alignment/server/) if you'd like. I'd recommend specifying an accurate refinment method, such as L-INS-i, and saving as a phylip file. You will want to align each gene seperately in MAFFT, which is why we created seperate alignment files beforehand. MAFFT is very easy to use, so I don't have any other advice to add here.

Afterwards, be sure to concatenate your alignment files in order to make the tree. I believe Biopython is a popular choice for this.

#### [IQ-TREE](http://www.iqtree.org)

I use [IQ-TREE](http://www.iqtree.org)'s webserver rather than running it locally, located [here](http://iqtree.cibiv.univie.ac.at) (though, there's actually a couple different servers). You'll give it your concatenated alignment file, and then run the tree. Again, very simple to run, no extra advice needed.

Afterwards, feel free to date you tree however you'd like. It's useful (but optioinal) to be dated for later analysis.

#### [prune_species.R](prune_species.R)

If you have any species you would like to prune from the tree (maybe they didn't have complete mitogenomes), now's the time to do so. Use [prune_species.R](prune_species.R) by going into the file and editing the parameters to fit your needs. Then, just run it as is.

For instance, here were my parameters:
```
tree_file <- 'unpruned_dated.tree'

species_to_drop <- c("ANT056", "ANT075")

updated_file_name <- 'pruned_dated.tree'
```

### 5. Ancestral State Reconstruction
Dependency: [phytools](https://github.com/liamrevell/phytools)

#### [plotASR.R](plotASR.R)

Use [plotASR.R](plotASR.R) by editing the parameters in the file, such as before. These parameters are more complicated, so I will explain the complex ones here.

```
traits_table_file <- "traits_table_binary.csv"
```
traits_table_file is a csv with columns 'Sample', 'GeneOrder' and 'Species'. You can easily create this csv from the one produced by [gene_order.py](gene_order.py), just add your species information and change any updated column names. 

For example, it should look something like this:

| Sample | GeneOrder | Species              |
|--------|-----------|----------------------|
| S001   | A         | Swiftia exserta      |
| S002   | B         | Muricea pendula      |
| S003   | A         | Plexaura kuna        |

```
colors <- c("black","red")
```
colors is a vector of the colors you'd like to assign to gene orders in your reconstructed tree. With the example from above, A would be colored black and B would be colored red. Make sure the number of colors you choose matches the number of unique gene orders found. 

Specific to octocorals, you may wish to do analysis of ancestral gene orders vs. other gene orders. This is what I did, and I set all non-ancestral gene orders to 'O', for 'Other'. That way, you just need two colors.

```
root_probs <- c(1,0)
```
root_probs is a vector of the probabilities of the root's gene order. With the example from above, A would be fixed at the root with 100% probability. You may leave this blank, but you should go edit the ASR call in the file accordingly. 

For octocorals, you may wish to fix the ancestral order at the root of your tree, as I did.

```
tree_type <- "fan"
```
Simply set tree_type to "fan" or "phylogram", and it will output accordingly.


After you check all the parameters you wish, run the code and it will show you your tree!

### Further Analysis

If you'd like to take things a step further, you can look at my analysis code for inspiration. I was interested in whether gene order (A vs O) is dependent on branch length, so I conducted a two sample t test on my data. You can check out that code here [gene_order_analysis.R](gene_order_analysis.R), though you will have to change the paramters to fit your data. This code will conduct a t test as stated and produce some other summary statistics for you to look at. If you have any questions or interesting thoughts, reach out to me!




The project was funded under a NOAA OER grant to C. McFadden, A. Quattrini and S. Herrera.

Example files are provided for ease of use, these don't represent any actual findings from this project.

Feel free to use code for your own purposes, but please cite as according to the [citation file](CITATION.cff).

Please reach out to me [kmitchell@hmc.edu](mailto:kmitchell@hmc.edu) with anything you need help on.
