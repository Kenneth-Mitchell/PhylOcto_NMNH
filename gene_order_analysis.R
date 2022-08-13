# likelihood of an altered gene order based on the age of a node
library(ggplot2)
tree_file <-'pruned_dated.tree'

traits_table_file <- "traits_table_binary.csv"

tips <- c("S001","S002","S003","S004","S005","S006","S007","S008","S009","S010","S011","S012","S013","S014","S015","S016","S018","S019","S020","S030","S031","S032","S033","S034","S035","S036","S037","S038","S042","S043","S044","S045","S046","S047","S048","S049","S050","S052","S055","S056","S057","S058","S062","S063","S066","S067","S068","S069","S071","S073","S074","S075","S080","S081","S082","S083","S084","S085","S086","S087","S088","S089","S090","S091","S092","S093","S094","S095","S096","S097","S098","S099","S100","S101","S102","S103","S104","S105","S106","S107","S108","S109","S110","S111","S112","S113","S114","S115","S116","S117","S118","S119","S121","S122","S123","S124","S125","S126","S127","S128","S129","S130","S131","S132","S133","ANT019","ANT020","ANT021","ANT022","ANT023","ANT024","ANT025","ANT026","ANT027","ANT029","ANT030","ANT031","ANT033","ANT034","ANT035","ANT036","ANT037","ANT038","ANT039","ANT040","ANT041","ANT043","ANT044","ANT045","ANT046","ANT047","ANT048","ANT049","ANT050","ANT051","ANT052","ANT053","ANT054","ANT055","ANT060","ANT061","ANT062","ANT064","ANT065","ANT066","ANT067","ANT068","ANT069","ANT070","ANT072","ANT073","ANT076","ANT077","ANT080","ANT081","ANT082","ANT083","ANT084","ANT085","ANT097","ANT098","ANT099","ANT100","ANT101","ANT102","ANT104","ANT105","ANT106","ANT107","ANT108","ANT109","ANT112","ANT113","ANT114","ANT115","ANT116","ANT117","ANT170","ANT171","ANT172","ANT173","ANT174","ANT175","ANT176","ANT177","ANT178","ANT179","ANT188","ANT276","ANT028","ANT079","ANT032","ANT058","ANT059","ANT074","ANT078","ANT111","ANT287","ANT288")

t<-read.tree(tree_file)

nodes<-sapply(tips,function(x,y) which(y==x),y=t$tip.label)

edge.lengths<-setNames(t$edge.length[unlist(sapply(nodes,function(x,y) which(y==x),y=t$edge[,2]))],names(nodes))

x=read.csv(traits_table_file, row.names=1)

geneorders <- x$GeneOrder[match(names(edge.lengths), rownames(x))]

edge.lengths<- log10(edge.lengths)

geneorder_lengths <- tibble(geneorders, edge.lengths)

geneorder_lengths %>% ggplot() + geom_histogram(aes(edge.lengths)) + facet_grid(~geneorders)

geneorder_lengths %>% group_by(geneorders) %>% summarize(mean=mean(edge.lengths))

A_lengths <- geneorder_lengths %>% filter(geneorders=='A') %>% select(edge.lengths)

O_lengths <- geneorder_lengths %>% filter(geneorders=='O') %>% select(edge.lengths)

t.test(A_lengths, O_lengths)
