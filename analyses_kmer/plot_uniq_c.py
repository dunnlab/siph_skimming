#!/usr/bin/env python3
"""
this script just makes a simple scatter plot from the output of
  sorted uniq -c on unix
"""
import argparse
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.min_rows', 35)
import sys

def argparser():
    """parses the arguments. Returns them as a dictionary."""
    parser = argparse.ArgumentParser(description='clustergenerator')
    parser.add_argument('-x', '--minX',
                        type=int,
                        help="""only plot the data starting at this X value""")
    parser.add_argument('-X', '--maxX',
                        type = int,
                        help = """only plot the window up to this X value""")
    parser.add_argument('--xlab', type = str,
                        default = "",
                        help = """x-label, in single quotes""")
    parser.add_argument('--ylab', type = str,
                        default = "",
                        help = """y-label, in single quotes.""")
    parser.add_argument('--title', type = str,
                        default = "",
                        help = """title, in single quotes.""")
    parser.add_argument('-d', '--dark',
                        action='store_true',
                        help = "make the plot over a dark background")
    parser.add_argument('-s', '--swap',
                        action='store_true',
                        help = "makes x col 0 and y col 1")
    parser.add_argument('-o', '--output',
                        default = None,
                        help = "save the plot here.")
    args = parser.parse_args()
    args = vars(args)
    return args

def main(args):
    mycolor='black'
    if args["dark"]:
        plt.style.use('dark_background')
        mycolor='#f2ecd0'

    thisx = 1
    thisy = 0
    if args["swap"]:
        thisx = 0
        thisy = 1

    df = pd.read_csv(sys.stdin, delim_whitespace=True, header=None)
    df = df.sort_values(thisx)
    df = df.reset_index(drop=True)
    #get the index of the first row where X >= minX
    mindex = int(df[df.iloc[:, thisx] >= args["minX"]].index[0])
    maxindex = int(df[df.iloc[:, thisx] <= args["maxX"]].index[-1])
    #print(mindex, maxindex)
    x = df.iloc[mindex:maxindex+1, thisx]
    y = df.iloc[mindex:maxindex+1, thisy]
    plt.plot(x, y, 'o', color = mycolor, ms=1);
    plt.title(args["title"])
    plt.xlabel(args["xlab"])
    plt.ylabel(args["ylab"])
    plt.xlim([0, args["maxX"]])
    #print(y)
    plt.ylim([0, max(y[3::])*1.25])
    plt.tight_layout()
    if args["output"] != None:
        outfile = args["output"]
    else:
        outfile =  'read_depth_histogram.pdf'
    plt.savefig(outfile)
    print("saved plot to {}".format(outfile))
if __name__ == "__main__":
    args = argparser()
    sys.exit(main(args))
