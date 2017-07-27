'''
Author: Thomas Goodman / Dominic Fitzgerald

This program takes fastqs that are 100bp and trims them to only be 50 bp

takes 1 or more fastqs as input, and a directory to output them to

'''

import os
import argparse
import gzip

GOOD_SEQ_LENGTH = 50

parser = argparse.ArgumentParser()
parser.add_argument('--fastqs', nargs='*')
parser.add_argument('--output')
args = vars(parser.parse_args())

print args['fastqs']
outdir = args['output']

for fastq_gz in args['fastqs']:
    with gzip.open(fastq_gz) as fastq:
        # Check out the second line to see if it's 100bp
        first_header = next(fastq)
        first_seq = next(fastq)
        if len(first_seq.strip()) <= GOOD_SEQ_LENGTH:
            continue
        first_seq = first_seq[:GOOD_SEQ_LENGTH] + '\n'

        # We need to trim this, open up a new file for writing
        fastq_filename = fastq_gz.split('/')[-1]
        trimmed_fastq_gz_filepath = os.path.join(outdir, fastq_filename)
        trimmed_fastq_gz = gzip.open(trimmed_fastq_gz_filepath, 'wb')

        first_third_line = next(fastq)
        first_quality = next(fastq)[:GOOD_SEQ_LENGTH] + '\n'
        trimmed_fastq_gz.write(''.join([first_header, first_seq, first_third_line, first_quality]))

        for i, line in enumerate(fastq, start=5):
            if i % 2 == 1:  # Line is odd'
                trimmed_fastq_gz.write(line)
            else:
                trimmed_fastq_gz.write(line[:GOOD_SEQ_LENGTH] + '\n')

        trimmed_fastq_gz.close()