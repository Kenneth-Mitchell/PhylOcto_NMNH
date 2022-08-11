for d in ./*/;
do
        file="$d"*"MitoFinder_megahit_mitfi_Final_Results/"*".gb"

	info="$d"*"MitoFinder_megahit_mitfi_Final_Results/"*".infos"

        cp $file ./gb_files

	cp $info ./gb_files
done


