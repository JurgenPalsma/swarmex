import subprocess
import sys
import os

def dc_server(port, datafile):
    #print("Launching dc server on port: %s with file: %s" % (port, datafile))
    subprocess.call(['java', '-jar', 'dc-server.jar', datafile, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01', port ])

#java -jar dc-server.jar data/fx-spot_EUR_GBP_10min_201308.txt:fx-spot_EUR_GBP_10min_201308:0:20:21:27 1000 35 4 0.90 0.10 0.0025 5 200 500000 -1 0.2 3 1 0.01

if __name__== "__main__":

    if len(sys.argv) != 3:
        print("Using default args. Real usage: python dc-server.py <data file name> <jvm port>")
        DATA_FILE_PATH = 'data/fx-spot_EUR_GBP_10min_201310.txt'
        R_FILE_PATH = "results/pso/fx-spot_EUR_GBP_10min_201310/"
        GA_R_FILE_PATH = "results/ga/fx-spot_EUR_GBP_10min_201310"
        PORT = '27134'

    else:
        DATA_FILE_PATH = 'data/' + sys.argv[1] + '.txt'
        R_FILE_PATH = 'results/pso/' + sys.argv[1]  + '/'
        GA_R_FILE_PATH ='results/ga/' + sys.argv[1]
        PORT = sys.argv[2]
    
    if not os.path.exists(DATA_FILE_PATH):
        print("%s: File not found" % DATA_FILE_PATH)
        quit()

    dc_server(PORT, DATA_FILE_PATH + ':' + GA_R_FILE_PATH + ':0:20:21:27')
