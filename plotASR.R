library(dplyr)
library(phytools)

# parameters (to edit!)

tree_file <-'pruned_dated.tree'

traits_table_file <- "traits_table_binary.csv" #traits table is a csv with a column 'GeneOrder' and a column 'Species'

colors <- c("black","red") #choose a number of colors equal to the number of unique traits

root_probs <- c(1,0,0,0,0,0,0,0) #choose root probabilities for traits, if you want to

tree_type <- "fan" # "fan" or "phylogram"


#updating the species names
T <- read.tree(tree_file)

x=read.csv(traits_table_file, row.names=1)

x$full_name <- paste(rownames(x),x$Species) %>% gsub(' ','_',.) %>% sub("\\_+$", "", .) %>% sub("\\.+$", "", .)

T$tip.label <- x$full_name[match(T$tip.label, rownames(x))]


#Building the tree
ske<-setNames(x$GeneOrder,x$full_name)

cols=(setNames(colors, levels(ske))) 

mtrees<-make.simmap(T,ske,model="ER",nsim=100, pi=root_probs)
pd<-summary(mtrees,plot=FALSE)



#Plotting ASR and time scaled tree
library(plotrix)
par(bg='transparent')
if (tree_type == 'fan') {
  plot(pd, cols,type="fan",fsize=.3, ftype="i", part=.99,lwd=0.5,offset=20,cex=c(.5,.2))
} else {
  plot(pd, cols,type="phylogram",fsize=.2, ftype="i", part=.99,lwd=0.5,offset=1,cex=c(.1,.1))
}

