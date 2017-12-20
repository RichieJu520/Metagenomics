# -*- coding: utf-8 -*-
"""
@author: Feng Ju
@email: richieju520@gmail.com
The script was written and tested in python 2.7 and biopython 1.58
"""

try:  
    from Bio import SeqIO
except:
    print "Please install biopython before continue!"
        
import time, sys
import argparse


def safe_open(file, mode='r'):
    if mode not in ('r', 'w','rb','wb','rU'):
            raise IOError, 'open for writing not allowed'
    
    if file.endswith('.gz'):
            import gzip
            return gzip.open(file, mode)
    else:
            return open(file, mode)

def mean_value(List):
    return sum(List)/float(len(List))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='a script for Quality Control (QC) of Illumina Pair-End (PE) Reads <richieju520@gmail.com>')

    parser.add_argument('-f', '--forward_reads_fp',
                        help='The file path of input forward reads in FASTQ format.',required=True)

    parser.add_argument('-r', '--reverse_reads_fp',
                        help='The file path of input reverse reads in FASTQ format.',required=True)

    parser.add_argument('-a', '--max_ambig',
                        help='maxmium number of ambiguous bases. Default: 3',type=int,default=3)

    parser.add_argument('-L', '--min_seq_length',
                        help='minimum sequence length (bp). Default: 50',type=int,default=50)

    parser.add_argument('-q', '--average_quality',
                        help='minimum average quality, Default: 20',type=float,default=20)

    parser.add_argument('-F', '--phred_format',
                        help='format of phred quality score, Default: 33',choices=["33", "64"],default="33")

    parser.add_argument('-o', '--output_prefix',
                        help='The prefix of filtered fastq files.',required=True)

    args = parser.parse_args()
            
    if args.phred_format == "64":
            Format = 'fastq-illumina'
    else:
            Format = 'fastq'
    
    handle1 = safe_open(args.forward_reads_fp, 'rb')
    handle2 = safe_open(args.reverse_reads_fp, 'rb')
    write1 = safe_open(args.output_prefix+'.qc.1.fq', 'wb')
    write2 = safe_open(args.output_prefix+'.qc.2.fq', 'wb')
    SeqIO1 = SeqIO.parse(handle1, Format)
    SeqIO2 = SeqIO.parse(handle2, Format)
    i, j = 0, 0

    start=time.time()
    wrerr = sys.stderr.write
    
    while True:
            try:
                record1 = SeqIO1.next()
                record2 = SeqIO2.next()
                i += 1
            except:
                break

            if i%1000000==0:
                print i,'PE reads scanned!'

            phredQualityList1 = record1.letter_annotations['phred_quality']
            phredQualityList2 = record2.letter_annotations['phred_quality']

            if len(str(record1.seq)) < args.min_seq_length or len(str(record2.seq)) < args.min_seq_length:
                continue

            if str(record1.seq).count('N') > args.max_ambig or str(record2.seq).count('N') > args.max_ambig:
                continue

            if (mean_value(phredQualityList1) < args.average_quality) or (mean_value(phredQualityList2) < args.average_quality):
                continue
                
            write1.write(record1.format(Format))
            write2.write(record2.format(Format))
            j +=1

    print str(j)+'/'+str(i),'PE reads written!'
    write1.close()
    write2.close()

    end=time.time()
    wrerr("OK, QC filtering finished in %3.2f secs\n" % (end-start))
