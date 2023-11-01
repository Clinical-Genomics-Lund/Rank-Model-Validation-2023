#! bin/bash

#The arguments are:
#$1: ID list (text file, one ID per line).
#$2: Input files path, needs to have unzipped VCF files with scores.
#$3: Output files path.

cat $1 | while read id; do
inp_vcf="$2$id*" ;
out_vcf="$3$id.new_score_comp.vcf" ;
/usr/local/bin/singularity exec --bind /trannel --bind /fs1 /fs1/resources/containers/genmod.sif genmod compound $inp_vcf > $out_vcf ;
done