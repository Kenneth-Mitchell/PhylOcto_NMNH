from enum import Enum
from logging import raiseExceptions
from Bio import SeqIO
from gene_order_params import GeneOrder, expected_genes, start_gene
import argparse
import os
import sys
import csv


def find_gene_match(gene_in_sample,file):
    for gene in expected_genes:

        for gene_name in gene:

            if gene_name == gene_in_sample:
                return gene[0]

    print(f'Unexpected gene detected: {gene_in_sample} in file {file}. Continuing to complete gene order anyways...')
    return None

def get_gene_order(file, store_new = False):

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

                    gene_match = find_gene_match(gene_in_sample,file)
                    if gene_match:
                        gene_order.append(gene_match)

        missing_genes = []      
        for gene in expected_genes:
            gene_name = gene[0]
            if gene_name not in gene_order:
                missing_genes.append(gene_name)
        
        if missing_genes: 
            print(f"Missing genes {missing_genes} in file {file}. Moving to next sample...\n")
            return 'None'

        index = gene_order.index(start_gene)
        gene_order = tuple(gene_order[index:] + gene_order[:index])
        
        try: 
            gene_order = GeneOrder(gene_order).name

        except:
            
            print('Detected new gene order!\n')
            print(gene_order)
            print('\n')
            # print('If you would like to save new gene orders, specify --new_gene_orders')
            return 'New'
            # raise Exception('Program stopped by new gene order. add to params and continue')

        return gene_order


def get_info(file):
    f = open(file)
    lines = f.readlines()
    for line in lines:
        if 'Length: ' in line:
            length = line.split()[1]
        elif 'GC content: ' in line:
            GC_Content = line.split()[2]
        elif 'Circularization: ' in line:
            Circularization = line.split()[1]
    return length, GC_Content, Circularization



def main():
    parser = argparse.ArgumentParser(description='given a genbank formatted file or directory holding .gb files, returns the gene order for each ')
    parser.add_argument('file', type=str, help='a single .gb file or a directory holding .gb files (if in batch mode)')
    parser.add_argument('--name', type=str, help='what you would like to name the output file (default is based on the file(s) run)', default=None)
    parser.add_argument('--overwrite',  action='store_true', help='overwrites any existing gene order files')
    # parser.add_argument('--batch', action='store_true', help='batch mode. if included, give gene_order.py a dir full of the files you want to run')
    #parser.add_argument('--new_gene_orders', action='store_true', help='store new gene orders in gene_order_params (does not by default)', default=False)
    


    args = parser.parse_args()

    # if args.batch:
    list_of_files = os.listdir(args.file)
    dict_of_G_O = {}
    dict_of_info = {}
    for file in list_of_files:
        path = str(args.file) + '/' + str(file)
        if file.endswith(".infos"):
            file = file.removesuffix('.infos')
            info = get_info(path)
            if info:
                dict_of_info[file]= info
        elif file.endswith('.gb'):
            file = file.removesuffix('_mtDNA_contig.gb')
            gene_order = get_gene_order(path)
            if gene_order:
                dict_of_G_O[file]=str(gene_order)

    if args.name:
        fn = args.name

    else: 
        fn = args.file + '_gene_order'

    try:
        f = open(fn, 'x', encoding = "ISO-8859-1")
    except IOError:
        if not args.overwrite:
            raise Exception(f'Gene order file exist with name {fn}Did you mean to use --overwrite?')
        f = open(fn, 'w+', encoding = "ISO-8859-1")

    keys = list(set(list(dict_of_G_O.keys()) + list(dict_of_info.keys())))

    writer= csv.writer(f)
    
    writer.writerow(['Sample', 'Gene Order Identified', 'mtGenome Length', 'GC Content', 'Circularization'])
    

    for key in keys:
        print(key)
        print(dict_of_G_O[key])
        print(dict_of_info[key])
        # try:
        writer.writerow([str(key), dict_of_G_O[key], dict_of_info[key][0], dict_of_info[key][1], dict_of_info[key][2]])
        # except:
        #     try:
        #         writer.writerow([str(key), dict_of_G_O[key]])
        #     except:
        #         pass

    f.close()

if __name__ == '__main__':
    sys.exit(main())
