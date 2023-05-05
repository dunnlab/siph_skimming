import sys

amino_acid_dict = {
    'A': 'Ala',
    'R': 'Arg',
    'N': 'Asn',
    'D': 'Asp',
    'C': 'Cys',
    'Q': 'Gln',
    'E': 'Glu',
    'G': 'Gly',
    'H': 'His',
    'I': 'Ile',
    'L': 'Leu',
    'K': 'Lys',
    'M': 'Met',
    'F': 'Phe',
    'P': 'Pro',
    'S': 'Ser',
    'T': 'Thr',
    'W': 'Trp',
    'Y': 'Tyr',
    'V': 'Val',
}

def get_trna_product(name: str) -> str:
    # Example name: trnW(tca)
    return f'tRNA-{amino_acid_dict[name[3]]}'



# Converts a gff file to a table in the format specified at 
# https://www.ncbi.nlm.nih.gov/genbank/organelle_submit/#Features
def main(in_name: str) -> int:
    out_name = in_name.replace('.gff', '.table')

    last_seqid = ''

    with open(out_name, 'w') as out_file:
        # Loop through the gff file line by line
        for line in open(in_name):
            # Skip the header lines
            if line.startswith('#'):
                continue

            line = line.strip()
            # Split the line into a list of columns
            # Agalma_clausi    mitos    gene    1768    2490    1.884963957E8    +    .    Name=cox2
            columns = line.split('\t')
            seqid = columns[0]
            source = columns[1]
            type = columns[2]
            start = columns[3]
            end = columns[4]
            strand = columns[6]
            name = columns[8].split('=')[1]

            if seqid != last_seqid:
                #if seqid != '':
                #    out_file.write(f'\n')
                out_file.write(f'>Feature {seqid}\n')
                last_seqid = seqid
            
            if strand == '+':
                out_file.write(f'{start}\t{end}\t{type}\n')
            else:
                out_file.write(f'{end}\t{start}\t{type}\n')
            
            if type == 'gene':
                out_file.write(f'\t\t\tgene\t{name}\n')

                # Need to write CDS lines as well
                if strand == '+':
                    out_file.write(f'{start}\t{end}\tCDS\n')
                else:
                    out_file.write(f'{end}\t{start}\tCDS\n')
                out_file.write(f'\t\t\tproduct\t{name}\n')
                out_file.write(f'\t\t\ttransl_table\t4\n')
                #out_file.write(f'\t\t\tcodon_start\t1\n')

            elif type == 'tRNA':
                out_file.write(f'\t\t\tproduct\t{get_trna_product(name)}\n')
                out_file.write(f'\t\t\tnote\t{name}\n')
            else:
                out_file.write(f'\t\t\tproduct\t{name}\n')

    return 0


if __name__ == '__main__':
    in_name = sys.argv[1]
    sys.exit(main(in_name))