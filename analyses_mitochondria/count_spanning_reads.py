import argparse
import pysam



def count_spanning(bam_file_path, fasta_file_path):
    # Get the length of the reference and initialize a list to store the spanning coverage
    # Assuming a single reference sequence or using the first one if multiple
    with pysam.FastaFile(fasta_file_path) as fastafile:
        ref_length = fastafile.get_reference_length(fastafile.references[0])
        spanning = [0] * ref_length
        print(f"Reference {fastafile.references[0]} length: {ref_length}")

    # Open the BAM file
    with pysam.AlignmentFile(bam_file_path, "rb") as bamfile:
        # Iterate through each alignment
        for read in bamfile:
            # Process only mapped reads
            if not read.is_unmapped:
                current_ref_pos = read.reference_start
                # Parse the CIGAR string for "M" operations, ie matches
                for cig_op in read.cigartuples:
                    op, length = cig_op
                    if op == 0:  # "M" operation
                        # Increment the spanning positions for this "M" segment, excluding the last position
                        for pos in range(current_ref_pos, current_ref_pos + length - 1):
                            spanning[pos] += 1
                    # Advance current_ref_pos for all operations that consume the reference
                    if op in (0, 2, 3):  # "M", "D", "N" operations
                        current_ref_pos += length

    # Check and print positions not spanned by any read
    not_spanned_positions = [i for i, count in enumerate(spanning) if count == 0]
    if not_spanned_positions:
        print("Positions not spanned by any read (0-indexed):")
        print(not_spanned_positions)
    else:
        print("All positions are spanned by at least one read.")
    
    # Specify the output file name
    output_file_path = 'spanning_coverage.txt'

    # Open the file for writing
    with open(output_file_path, 'w') as outfile:
        # Write the header
        outfile.write("Index\tValue\n")
        # Iterate over the spanning list and write index and value
        for index, value in enumerate(spanning):
            outfile.write(f"{index}\t{value}\n")

    print(f"Spanning coverage written to {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of reads spanning each position in the reference. The result is a list of counts for each position, where each count indiacates the number of reads that span from that position to the next position to the right. Zeros indicate no spanning reads.")
    parser.add_argument("bam_file", help="Path to the BAM file with reads aligned to the reference.")
    parser.add_argument("fasta_file", help="Path to the reference FASTA file")
    
    args = parser.parse_args()
    
    count_spanning(args.bam_file, args.fasta_file)