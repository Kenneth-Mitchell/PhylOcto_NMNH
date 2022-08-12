# Positional arugments needed: location of reads, location of adapters
# Be sure to update trimmomatic path if needed!
if [[ $# -eq 2 ]] ; then
	for forward_read in $1/*R1; do
		reverse_read=${forward_read//R1/R2}
		java -jar trimmomatic-0.35.jar PE $forward_read $reverse_read trimmed_reads/$forward_read trimmed_reads/$forward_read trimmed_reads/$reverse_read trimmed_reads/$reverse_read ILLUMINACLIP:$2:2:30:10
	done
else
	echo "Insufficient arguments supplied. Need positional arguments location of reads, location of adapter."
	exit 1
fi