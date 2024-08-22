# Converts SeqEnd gff produced my gmap to coverage data (.wig file)

# Prepare

## Import modules
import numpy as np
import argparse

## Parse arguments

### Initialize parser
parser = argparse.ArgumentParser(description='This is a command line parser')

### Adding optional argument
parser.add_argument("-i", "--input", action="store", type=str) # .gff file
parser.add_argument("-p", "--output_plus", action="store", type=str) # + strand .wig file
parser.add_argument("-m", "--output_minus", action="store", type=str) # - strand .wig file
    
### Read arguments from command line
args = parser.parse_args()  

if args.input:
    input_filepath = args.input
    print("input file: " + str(input_filepath))
if args.output_plus:
    output_plus_filepath = args.output_plus
    print("output plus file: " + str(output_plus_filepath))
if args.output_minus:
    output_minus_filepath = args.output_minus
    print("output plus file: " + str(output_minus_filepath))

## Paths
#defined below already

## Constants
genome_len = 4641652 # extracted from https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3/

## Variables
plus_cov = np.zeros(genome_len, dtype=np.int32)
minus_cov = np.zeros(genome_len, dtype=np.int32)

# Body

## Reading and parsing gff line by line, adding coverage into plus_cov and minus_cov np arrays
with open(input_filepath, 'r') as in_file:
    for line in in_file:
        line = line.strip()
        if line.startswith('#'):
            continue
        else:
            line_array = line.split('\t')
            curr_start = np.int32(line_array[3].strip()) - 1 # converted to 0-based python-style interval start (included)
            curr_end = np.int32(line_array[4].strip()) # converted to 0-based python-style interval end (exluded)
            curr_strand = str(line_array[6].strip())
            if curr_strand == '+':
                for idx in range(curr_start, curr_end):
                    plus_cov[idx] += 1
            elif curr_strand == '-':
                for idx in range(curr_start, curr_end):
                    minus_cov[idx] += 1
in_file.close()
                    
## Writing down output files
with open(output_plus_filepath, 'w') as output_plus_file:
    output_plus_file.write('first stupid line'+'\n')
    output_plus_file.write('second stupid line'+'\n')
    for i in range(genome_len):
        line = str(plus_cov[i])
        output_plus_file.write(line+'\n')
        
output_plus_file.close()

with open(output_minus_filepath, 'w') as output_minus_file:
    output_minus_file.write('first stupid line'+'\n')
    output_minus_file.write('second stupid line'+'\n')
    for i in range(genome_len):
        line = str(minus_cov[i])
        output_minus_file.write(line+'\n')
        
output_minus_file.close()

        


