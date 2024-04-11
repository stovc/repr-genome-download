"""Take an NCBI assembly summary as input
Return download paths of latest, full, reference or representative genomes.
Return one genome per {taxonomic level}

Usage: python3 mk_download_paths.py {assembly_summary file} {taxonomic level}
"""

import sys
import pandas as pd
from ete3 import NCBITaxa


def get_parent_taxon(taxid):
    """Get NCBI taxid of a species
    Return the parent taxon of rank specified in `parent_rank`
    """

    lineage_taxid = taxa.get_lineage(int(taxid))  # get the lineage as a list of taxids
    ranks = taxa.get_rank(lineage_taxid)  # make a dictionary {taxid: taxon rank}

    parent_taxon = get_key(ranks, filter_rank)

    return parent_taxon


def get_key(dictionary, search_value):
    """Find and return dictionary key by its value"""
    searched_key = None
    for key, value in dictionary.items():
        if value == search_value:
            searched_key = key
    return searched_key


if __name__ == '__main__':

    # arguments
    data_path = sys.argv[1]
    filter_rank = sys.argv[2]

    # make a taxonomy object with information from NCBI taxonomy database
    taxa = NCBITaxa()
    taxa.update_taxonomy_database()

    df = pd.read_csv(data_path, sep='\t',
                     usecols=['refseq_category', 'taxid', 'version_status', 'assembly_level',  # we filter based on these
                              'ftp_path'],  # this we print in the end
                     on_bad_lines='warn')   # some lines in RefSeq assembly summary are incorrect. to avoid an error call

    # filter genomes to be complete, latest, and reference or representative
    df = df[df.refseq_category.isin(['reference genome', 'representative genome'])]
    df = df[df.version_status == 'latest']
    df = df[df.assembly_level == 'Complete Genome']
    print(df)

    df['parent_taxid'] = df.apply(lambda row: get_parent_taxon(row['taxid']), axis=1)
    print(df)

    # some species are not well classified and will have `NA` in the `parent_taxid` column. We drop them
    df = df.dropna()
    print(df)

    df = df.groupby('parent_taxid').first()
    print(df)

    dir_paths = list(df['ftp_path'])

    download_paths = open('download_paths.txt', 'w')
    for dir_path in dir_paths:
        file_name = dir_path.split('/')[-1] + '_genomic.gbff.gz'  # name of the last directory in the path + suffix
        file_path = dir_path + '/' + file_name + '\n'
        download_paths.write(file_path)

    download_paths.close()
