import argparse
parser = argparse.ArgumentParser()

#-db DATABSE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-db", "--hostname", help="Database name")
parser.add_argument("-u", "--username", help="User name")
parser.add_argument("-p", "--password", help="Password")
parser.add_argument("-size", "--size", help="Size", type=int)

args = parser.parse_args()

print( "Hostname {} User {} Password {} size {} ".format(
        args.hostname,
        args.username,
        args.password,
        args.size
        ))