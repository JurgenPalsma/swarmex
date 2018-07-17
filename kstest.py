from scipy.stats import ks_2samp
import numpy as np
import pandas as pd
import sys

"""
This script performs a KS test on fitness values to make sure that they are sampled from a similar sample distribution
Input files are csv fitness values
The files are generated from running the algorithms for 30 runs
"""

def main():
    # print command line arguments
    ga = pd.read_csv('data/ga-ks-values.csv',header=None)
    pso = pd.read_csv('data/pso-ks-values.csv',header=None)
    print(ks_2samp(ga[0], pso[0]))

if __name__ == "__main__":
    main()
