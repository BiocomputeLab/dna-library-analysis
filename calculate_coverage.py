#!/usr/bin/env python3.5

# Author: Matthew Tarnowski
# Date: 20221026

import pandas as pd
import sys

ref = sys.argv[1]

db = pd.read_csv(ref,names=["","qseqid","sseqid","bitscore","aln_len","bitscore_max"])
bc = ref.split(".")[0] # .split("/")[2]
db = pd.DataFrame(db.groupby("qseqid").size())
db = db.reset_index()
db.columns=["ID","Count"]

#add in designs with no reads
all = pd.read_csv("../all_designs.csv")
db = db.merge(all, left_on="ID",right_on="ID",how="outer")
db["Count"] = db["Count"].fillna(0.0)

# format dataset
db["Spacer"] ="A"+db["ID"].str.slice(1,3)
db["Modifier"] ="B"+db["ID"].str.slice(5,7)
db["Terminator"] ="C"+db["ID"].str.slice(9,11)
db = db.reindex(columns = [col for col in db.columns if col != 'Count'] + ['Count'])
db["Freq_pc"] = db["Count"]/db["Count"].sum()
db["Freq_pc"] = db["Freq_pc"]
db.to_csv("../summary_data_40k/%s.csv" % bc, index=False)

#calculate number designs detected
thresh = (100/1000000)
print(ref, (db.Freq_pc.dropna()>thresh).values.sum())

del db