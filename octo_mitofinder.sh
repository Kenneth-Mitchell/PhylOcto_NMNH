# Positional arugments needed: location of reads, location of database
# Be sure to update mitofinder path if needed!
if [[ $# -eq 2 ]] ; then
	for forward_read in $1/*R1; do
		reverse_read=${forward_read//R1/R2}
		mitofinder -j $forward_read -1 $forward_read -2 $reverse_read -r $2 -o 4 -p 5 --new-genes --max-contig 1
	done
else
	echo "Insufficient arguments supplied. Need positional arguments location of reads, location of database."
	exit 1
fi