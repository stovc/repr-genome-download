#!/bin/bash

# Directory to download genomes to
DIR=$1

# Taxonomic rank to pick representatives for. Can be [superkingdom, phylum, class, order, family, genus, species]
FILTER_RANK=$2

REP=$(pwd)
cd $DIR

# Download assembly summary for bacteria, archaea, and viruses

wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt -O as_bacteria.tsv
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt -O as_archaea.tsv
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/viral/assembly_summary.txt -O as_viral.tsv

# concatenate without the first comment line
awk FNR!=1 as_* > assembly_summary.tsv

# remove downloaded assembly summaries
rm as_*

# make download paths. assembly summary is filtered to pick one representative 
python3 $REP/mk_download_paths.py $DIR/assembly_summary.tsv $FILTER_RANK

wget -i download_paths.txt

rm download_paths.txt
rm assembly_summary.tsv
