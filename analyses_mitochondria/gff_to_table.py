import sys
from statistics import mean

class feature:
    def __init__(self, seqid, source, type, start, end, score, strand, phase, name):
        self.seqid = seqid
        self.source = source
        self.type = type
        self.start = int(start)
        self.end = int(end)
        self.score = score
        self.strand = strand
        self.phase = phase
        self.name = name
    
    def length(self):
        return self.end - self.start + 1

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

    feature_list = []

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
            score = columns[5]
            strand = columns[6]
            phase = columns[7]
            name = columns[8].split('=')[1]

            # Create a feature object and add it to the list
            feature_list.append(feature(seqid, source, type, start, end, score, strand, phase, name))

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

    # validate the features
    # loop over the unique seqids
    for seqid in set([f.seqid for f in feature_list]):
        # get the features for this seqid
        seqid_features = [f for f in feature_list if f.seqid == seqid]
        # Check if any of the features overlap
        for i in range(len(seqid_features)):
            for j in range(i+1, len(seqid_features)):
                if seqid_features[i].start <= seqid_features[j].end and seqid_features[i].end >= seqid_features[j].start:
                    print(f'Features overlap on {seqid}')
                    print(f'  Feature 1: {seqid_features[i].type} {seqid_features[i].name} {seqid_features[i].start} {seqid_features[i].end}')
                    print(f'  Feature 2: {seqid_features[j].type} {seqid_features[j].name} {seqid_features[j].start} {seqid_features[j].end}')
                    # return 1
        
    # Check if any seqids have more than one feature with the same name
    # loop over the unique seqids
    for seqid in set([f.seqid for f in feature_list]):
        # get the features for this seqid
        seqid_features = [f for f in feature_list if f.seqid == seqid]
        # loop over the unique feature names
        for name in set([f.name for f in seqid_features]):
            # get the features for this name
            name_features = [f for f in seqid_features if f.name == name]
            if len(name_features) > 1:
                print(f'Error: {seqid} has more than one feature with name {name}')
                for f in name_features:
                    print(f'  {f.type} {f.start} {f.end}')
                # return 1

    # loop over the unique feature names
    for name in set([f.name for f in feature_list]):
        # For this feature name, construct a dictionary for all the features with this name
        # where the key is the seqid and the value is the length of the feature
        lengths_dict = {}
        for f in [f for f in feature_list if f.name == name]:
            if f.seqid not in lengths_dict:
                lengths_dict[f.seqid] = []
            lengths_dict[f.seqid].append(f.end - f.start + 1)
        print(f'Feature {name} has lengths:')
        # create a set of seqids for this feature namme that have a length more than 10%
        # longer then the mean length for this feature name
        long_seqids = set()
        for seqid in lengths_dict:
            if max(lengths_dict[seqid]) > 1.1 * mean(lengths_dict[seqid]):
                long_seqids.add(seqid)
        
        # print the seqqid and length for each feature in descending order of length
        for seqid in sorted(lengths_dict, key=lambda x: max(lengths_dict[x]), reverse=True):
            # add an * end of the line if this seqid is in the long_seqids set
            if seqid in long_seqids:
                print(f'  {seqid} {max(lengths_dict[seqid])} *')
            else:
                print(f'  {seqid} {max(lengths_dict[seqid])}')

    return 0


if __name__ == '__main__':
    in_name = sys.argv[1]
    sys.exit(main(in_name))