#YOUR_SHEBANG_HERE

ID_list=$1 #The text file with the case IDs.
rank_model_name=$2 #This is just a string for folder and file names.
rank_model_file=$3 #The .ini file.
no_score_path=$4 #The VCF file(s) with no score fields in them.
output_path=$5
is_trio=$6 #Should be yes or no

#Create the required folders.
#Modified model path:
newdir=$output_path$rank_model_name"/"
mkdir -p $newdir

#Create the plot folder.
plot_path=$newdir"plots/"
mkdir -p $plot_path

is_trio=$(echo $is_trio | tr '[:upper:]' '[:lower:]')

if [[ $is_trio == "y" || $is_trio == "yes" ]]; 
    then threshold=19
    first_score_path=$newdir"no_compound_correction_vcf/" #First scores output (no compund correction):
    mkdir -p $first_score_path
    final_score_path=$newdir"vcf/"
    mkdir -p $final_score_path
    bash /YOUR_SCRIPT_DIR/run_rank_model.sh $ID_list $rank_model_file $no_score_path $first_score_path
    bash /YOUR_SCRIPT_DIR/compound_effect.sh $ID_list $first_score_path $final_score_path
    rm -r $first_score_path
elif [[ $is_trio == "n" || $is_trio == "no" ]]; 
    then threshold=17
    final_score_path=$newdir"vcf/";
    mkdir -p $final_score_path;
    bash /YOUR_SCRIPT_DIR/run_rank_model.sh $ID_list $rank_model_file $no_score_path $final_score_path; fi
else echo "Please enter y/Y/yes/Yes or n/N/no/No"; exit 1 ; fi

#g-zip the VCF-files so that they take less space:
gzip $final_score_path*.vcf

YOUR_PYTHON_DIR /YOUR_SCRIPT_DIR/get_data_from_VCF.py $ID_list $final_score_path #Extract the relevant data from the VCF-file to a text file.

YOUR_PYTHON_DIR /YOUR_SCRIPT_DIR/validation.py $ID_list $rank_model_name $final_score_path $newdir $threshold #Run the bootstrap.

YOUR_PYTHON_DIR /YOUR_SCRIPT_DIR/plot_vcf.py $ID_list $final_score_path $plot_path $rank_model_name $threshold $is_trio #Plot the results from the datafile (not the bootstrap results).

YOUR_PYTHON_DIR /YOUR_SCRIPT_DIR/plot_bootstrap_results.py $rank_model_name $newdir