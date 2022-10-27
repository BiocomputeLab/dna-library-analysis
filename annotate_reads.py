#!/usr/bin/env python3.5

# Author: Matthew Tarnowski
# Date: 20221026

import sys
import pandas as pd

lib_aln_file = sys.argv[1]
output_file = sys.argv[2]

df_filt = pd.read_csv(lib_aln_file,names=["","qseqid","sseqid","bitscore","aln_len","bitscore_max"])

#filter the filtered file so that each read is assigned the barcode with the best evalue
df_filt["bitscore_max"] = df_filt.groupby(["sseqid"])["bitscore"].transform(max)
best_aln = df_filt[df_filt.bitscore_max == df_filt.bitscore]

#remove ambiguous alignments
best_aln = best_aln.drop_duplicates(subset="sseqid",keep=False)

#save file
best_aln.to_csv("%s" % output_file)

del best_aln,df_filt