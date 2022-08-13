# Positional arugments needed: location of Mitofinder results
# Be sure to update mitofinder pathing if your result files are named something else for any reason (such as using a different assembly).
if [[ $# -eq 1 ]] ; then
	for d in $1/*/; do
                file="$d"*"MitoFinder_megahit_mitfi_Final_Results/"*".gb"
                info="$d"*"MitoFinder_megahit_mitfi_Final_Results/"*".infos"
                cp $file ./gb_files
                cp $info ./gb_files
        done
else
	echo "Insufficient arguments supplied. Need positional argument location of Mitofinder results.
	exit 1
fi



