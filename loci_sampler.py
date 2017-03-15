#!/usr/bin/env python2

import sys

filename = sys.argv[1]
locus_header = filename.split('.')[0]+"-locus"
try: minsample = int(sys.argv[2])
except (ValueError, IndexError): minsample = 4

with open(filename) as locifile:
    seq = ''
    loci = []
    seqs = {}
    loc_depth = 0
    for line in locifile:
        if line[0] != "/":
            seq = line.strip("\n").split()[1].replace("-","")
            loc_depth += 1
            if seq in seqs:
                seqs[seq] += 1
            else:
                seqs[seq] = 1
        elif line[0] == "/":
            if loc_depth >= minsample:
                locusname = ">" + locus_header + line.strip("\n").split("|")[1].zfill(6) # change fill parameter
                loci.append(locusname)
                loci.append(max(seqs.iterkeys(), key=(lambda key: seqs[key])))
            seq = ''
            seqs = {}
            loc_depth = 0

loci_number = str(len(loci)/2)
if filename.split('.')[-1] == 'alleles':
    minsample = minsample/2
outfile = open(filename.split('.')[0]+"_min"+str(minsample).zfill(2)+"_"+loci_number+"loci_dups.fasta", "w")
outfile.write("\n".join(loci)+"\n")
outfile.close()
