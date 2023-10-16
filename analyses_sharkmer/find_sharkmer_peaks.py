import argparse
import glob
import os
import numpy as np
import pandas as pd
import scipy.signal

def find_peaks(input_dir):
    # Loop over all .histo files in input_dir
    file_pattern = '*sharkmer.histo'
    histo_files = glob.glob(os.path.join(input_dir, file_pattern))
        
    for histo_file in histo_files:
        df_histo = pd.read_csv(histo_file, sep="\s+", header=None, engine='python')
        
        # Assuming the first column is 'count' and the next 100 columns are percentiles
        for percentile in range(1, 101):  # Columns 1 to 100
            y = np.array(df_histo[percentile])
            peaks, properties = scipy.signal.find_peaks(y, height=0, distance=2, threshold=10)
            
            # Create a numpy array as long as y filled with zeros, then set the peak positions to 1
            peaks_array = np.zeros(len(y))
            peaks_array[peaks] = 1
            
            # Add the peaks_array as a new column to the dataframe
            column_name = f'peaks_{percentile}'
            df_histo[column_name] = peaks_array

            # If you only want to keep records of peaks, you might want to filter the DataFrame here
            
        # Write the dataframe to a new file
        df_histo.to_csv(histo_file + '.peaks', sep="\t", header=None, index=False)
        
        # If you want to perform further analysis or printing for each file, do it here

def main():
    parser = argparse.ArgumentParser(description="Look for peaks in kmer distributions")
    parser.add_argument(
        "-i", "--input",
        help="Input folder containing .histo files",
        required=True
    )
    
    args = parser.parse_args()
    
    find_peaks(args.input)

if __name__ == "__main__":
    main()
