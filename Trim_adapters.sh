for forward_read in *R1_001.fastq.gz; do
	reverse_read=${forward_read//R1/R2}
	java -jar /data/mcfadden/aquattrini/PROGRAMS/Trimmomatic-0.35/trimmomatic-0.35.jar PE $forward_read $reverse_read /data/mcfadden/smoaleman/coral_mitchell_2022/data/trimmed_reads/$forward_read /data/mcfadden/smoaleman/coral_mitchell_2022/data/trimmed_reads/$forward_read /data/mcfadden/smoaleman/coral_mitchell_2022/data/trimmed_reads/$reverse_read /data/mcfadden/smoaleman/coral_mitchell_2022/data/trimmed_reads/$reverse_read ILLUMINACLIP:/data/mcfadden/smoaleman/coral_mitchell_2022/data/trim_test/adapters.fasta:2:30:10
done
