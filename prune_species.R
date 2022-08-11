
library(ape)
library(phytools)
# parameters (to edit!)
tree_file <- 'pruned_dated.tree'

species_to_drop <- c("ANT056", "ANT075")

updated_file_name <- 'pruned_dated.tree'

#pruning
uceocto=read.nexus(tree_file)

pruned.tree<-drop.tip(uceocto,uceocto$tip.label[match(species_to_drop, uceocto$tip.label)])
write.tree(pruned.tree, updated_file_name)
