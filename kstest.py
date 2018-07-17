from scipy.stats import ks_2samp
import numpy as np
import pandas as pd
import sys

"""
This script performs a KS test on fitness values to make sure that they are sampled from a similar sample distribution
Input files are csv fitness values

"""

def main():
    # print command line arguments
    ga = pd.read_csv('ga-ks-values.csv',header=None)
    pso = pd.read_csv('pso-ks-values.csv',header=None)
    print(ks_2samp(ga[0], pso[0]))

if __name__ == "__main__":
    main()


"""
np.random.seed(12345678)
x = np.random.normal(0, 1, 1000)
y = np.random.normal(0, 1, 1000)

print(ks_2samp(x, y))
"""