#!/bin/bash

#The arguments are:
#$1: ID_list (text file, one ID per line)
#$2: Rank model
#$3: Input files path. Should contain VCF files with no scores! They should also be unzipped.
#$4: Output files path

cat $1 | while read id; do
vcf="$3$id*" ;
out="$4$id.new.score.vcf" ;
/usr/local/bin/singularity exec --bind /trannel --bind /fs1 /fs1/resources/containers/genmod.sif genmod score -i $id -c $2 -r $vcf -o $out ;
done
