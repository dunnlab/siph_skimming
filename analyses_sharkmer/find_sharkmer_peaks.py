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
        
        # Only retain the first n rows
        n = 100
        df_histo = df_histo.head(n)

        # Prepare DataFrames to store new columns and peak summaries
        new_columns = pd.DataFrame(index=np.arange(len(df_histo)))  # it should have the same number of rows as df_histo
        peaks_data = []

        # Assuming the first column is 'count' and the next 100 columns are percentiles
        for percentile in range(1, 101):  # Columns 1 to 100
            y = np.array(df_histo[percentile])
            peaks, _ = scipy.signal.find_peaks(y, height=100000, distance=2, threshold=20)

            # Create a numpy array as long as y filled with zeros, then set the peak positions to 1
            peaks_array = np.zeros(len(y))
            peaks_array[peaks] = 1

            # Store new column data
            new_columns[f'peaks_{percentile}'] = peaks_array
            
            # Add peak information for concatenation later
            for peak in peaks:
                peak_info = {
                    'percentile': percentile,
                    'count': df_histo.iloc[peak, 0],
                    'num_kmers': df_histo.iloc[peak, percentile]
                }
                peaks_data.append(pd.DataFrame([peak_info]))

        # Concatenate all new columns into the original DataFrame
        df_histo = pd.concat([df_histo, new_columns], axis=1)

        # Write the dataframe to a new file
        df_histo.to_csv(histo_file + '.peaks', sep="\t", header=None, index=False)

        # Concatenate all the individual DataFrame slices (for each peak) into a single DataFrame
        if peaks_data:
            peaks_summary = pd.concat(peaks_data, ignore_index=True)
            # Write the peaks summary to a new file
            peaks_summary.to_csv(histo_file + '.peaks.summary', sep="\t", index=False)
            

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
