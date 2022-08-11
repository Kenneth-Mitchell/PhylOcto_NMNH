
for read in /data/mcfadden/smoaleman/coral_mitchell_2022/data/cleanreads/ANT*; do
	echo -e "Beginning $read ...\n"

	read1=("$read/split-adapter-quality-trimmed/"*"READ1.fastq"*)
        read2=("$read/split-adapter-quality-trimmed/"*"READ2.fastq"*)

	if [[ -f  $read1 ]]; then
		echo -e "forward read found: $read1\n"
	elif [[ -f $read1.gz ]]; then
		echo -e "forward read found as zip: $read1.gz\n"
		read1="$read1.gz"
	else
		echo  "ERROR: forward read not found in path $read1"
		exit 1
	fi

	if [[ -f $read2 ]]; then
                echo -e "reverse read found: $read2\n"
        elif [[ -f $read2.gz ]]; then
                echo -e "reverse read found as zip: $read2.gz\n"
                read2="$read2.gz"
        else
                echo "ERROR: reverse read not found in path $read2"
                exit 1
	fi

	output=$read/output_GetOrganelle

	python /data/mcfadden/smoaleman/coral_mitchell_2022/programs/GetOrganelle/get_organelle_from_reads.py -1 $read1 -2 $read2 -o $output -s /data/mcfadden/smoaleman/coral_mitchell_2022/data/database/mutS.fasta  -F animal_mt --overwrite

	echo -e "$read is done!\n"
done

