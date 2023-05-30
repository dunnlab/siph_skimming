import argparse
import glob
import numpy as np
import pandas as pd
import scipy

def find_peaks(input_dir):
    # loop over all .histo files in input_dir
    file_pattern = '*.histo'
    histo_files = glob.glob(input_dir + '/' + file_pattern)
        
    for histo_file in histo_files:
        df_histo = pd.read_csv(histo_file, sep="\s", header=None, engine='python')
        y = np.array(df_histo[1])
        peaks, properties = scipy.signal.find_peaks(y, height=0, distance=2, threshold=10)
        # Create a numpy array as long as y filled with zeros, then set the peak positions to 1
        peaks_array = np.zeros(len(y))
        peaks_array[peaks] = 1
        # Add the peaks_array as a new column to the dataframe
        df_histo['peaks'] = peaks_array
        # Write the dataframe to a new file
        df_histo.to_csv(histo_file + '.peaks', sep="\t", header=None, index=False)
        
        print(histo_file)
        # print each row of df_histo that has an index less than 100 and a peak value > 0
        peak_rows = df_histo[(df_histo.index < 100) & (df_histo['peaks'] > 0)]
        if len(peak_rows) > 0 and not peak_rows.empty:
            print(peak_rows)
        else:
            print("No peaks found")

        

def main():
    # https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser(description="look for peaks in kmer distributions")
    parser.add_argument(
        "-i", "--input",
        help="input folder containing .histo files",
        required=True
    )
    
    args = parser.parse_args()
    
    find_peaks(args.input)


if __name__ == "__main__":
    main()
