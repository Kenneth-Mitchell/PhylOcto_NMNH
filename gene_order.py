from enum import Enum
from logging import raiseExceptions
import pandas as pd
from Bio import SeqIO
from gene_order_params import GeneOrder, expected_genes, start_gene
import argparse
import os
import sys


def gene_order(file, store_new = False):

    with open(file) as handle:
        for sample in SeqIO.parse(handle, "genbank"):
            gene_order = []
            for feature in sample.features:
                if feature.type == 'gene':
                    try:
                        gene_in_sample = feature.qualifiers['gene'][0].lower()

                    except:   
                        try: 
                            gene_in_sample = feature.qualifiers['product'][0].lower()

                        except:
                            break

                    for genes in expected_genes:

                            for gene in genes:

                                if gene == gene_in_sample:
                                    gene_order.append(genes[0])
                            

        index = gene_order.index(start_gene)
        gene_order = tuple(gene_order[index:] + gene_order[:index])
        
        try: 
            gene_order = GeneOrder(gene_order).name

        except:
            
            print('Detected new gene order!\n')
            print(gene_order)
            print('\n')
            # print('If you would like to save new gene orders, specify --new_gene_orders')
                
            raise Exception('Program stopped by new gene order. add to params and continue')

        return gene_order



def main():
    parser = argparse.ArgumentParser(description='given a genbank formatted file or directory holding .gb files, returns the gene order for each ')
    parser.add_argument('file', type=str, help='a single .gb file or a directory holding .gb files (if in batch mode)')
    parser.add_argument('--name', type=str, help='what you would like to name the output file (default is based on the file(s) run)', default=None)
    parser.add_argument('--overwrite',  action='store_true', help='overwrites any existing gene order files')
    parser.add_argument('--batch', action='store_true', help='batch mode. if included, give gene_order.py a dir full of the files you want to run')
    #parser.add_argument('--new_gene_orders', action='store_true', help='store new gene orders in gene_order_params (does not by default)', default=False)
    


    args = parser.parse_args()

    if args.batch:
        list_of_files = os.listdir(args.file)
        list_of_G_O = []
        for file in list_of_files:
            file = str(args.file) + '/' + str(file)
            list_of_G_O.append((file, str(gene_order(file))))
    else:
        list_of_G_O.append((file, str(gene_order(file))))

    if args.name:
        fn = args.name

    else: 
        fn = args.file + '_gene_order'

    try:
        f = open(fn, 'x', encoding = "ISO-8859-1")
    except IOError:
        if not args.overwrite:
            raise Exception('gene order file exist with name ' + fn +'. Did you mean to use --overwrite?')
        f = open(fn, 'w+', encoding = "ISO-8859-1")

    for file, g_o in list_of_G_O:

        f.write(file)
        f.write('\n')
        f.write(g_o)
        f.write('\n')

    f.close()

if __name__ == '__main__':
    sys.exit(main())