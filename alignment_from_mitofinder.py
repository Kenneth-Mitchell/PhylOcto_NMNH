import sys
import os
import argparse




#========================================
# functions

def load(filename):
    """Load fasta or multifasta.
    
    Parameters
    --------------------
      fn -- filename of fasta file
    
    Return
    --------------------
      fa -- list of tuples (key, seq)
    """
    
    fa = []
    temp_header = ''
    temp_seq = ''

    with open(filename,"r", encoding = "ISO-8859-1") as f:
        for line in f:
            if line[0] == '>':
                if not temp_header == '' and not temp_seq == '':
                    fa += [(temp_header.replace('\n',''),temp_seq.replace('\n',''))] # adds in our header/seq pair and removes any newline chars from the seq.
                    temp_seq = ''
                temp_header = line[1:]
            else: 
                temp_seq += line
            
    
    if not temp_header == '' and not temp_seq == '': # Do this again at the end to catch the last pair of header/seq
       fa += [(temp_header.replace('\n',''),temp_seq.replace('\n',''))]
    
    f.close()
    return fa


#========================================
# main

def main():
    parser = argparse.ArgumentParser(description='given a directory holding fasta files, creates an alignment file for each unique gene. \n (made to be used with mitofinder results)')
    parser.add_argument('dir', type=str, help='the directory holding fasta files')
    parser.add_argument('--overwrite',  action='store_true', help='overwrites any existing alignment files')

    args = parser.parse_args()

    path = args.dir

    # process input
    path = sys.argv[1]
    fa = []
    list_of_files = os.listdir(path)
        
    for file in list_of_files:
        fa += load(str(path) + '/' + str(file))  # load file

    unique_genes = []

    for key,seq in fa:
        
        gene = key.split('@')[1]
        
        if gene not in unique_genes:
            unique_genes.append(gene)
            try:
                f = open(gene, 'x', encoding = "ISO-8859-1")
            except IOError:
                if not args.overwrite:
                    raise Exception('Alignment files exist with name ' + key +'. Did you mean to use --overwrite?')
                f = open(gene, 'w+', encoding = "ISO-8859-1")
        else:
            f = open(gene, 'a+', encoding = "ISO-8859-1")
            
        f.write(">%s" % key)
        f.write('\n')
        f.write(seq)
        f.write('\n')
        f.close()

if __name__ == '__main__':
    sys.exit(main())
