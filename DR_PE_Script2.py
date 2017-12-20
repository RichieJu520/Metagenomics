"""
@author: Feng Ju
@email: richieju520@gmail.com
The script was written and tested in python 2.7 and biopython 1.58
"""

try:  
    from Bio.SeqIO.QualityIO import FastqGeneralIterator
except:
    print "Please install biopython before continue!"

import itertools        
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

if __name__ == '__main__':

        parser = argparse.ArgumentParser(description='a script for De-Replication of Pair-End (PE) Reads <richieju520@gmail.com>')

        parser.add_argument('-f', '--forward_reads_fp',
                        help='The file path of input forward reads in FASTQ format.',required=True)

        parser.add_argument('-r', '--reverse_reads_fp',
                        help='The file path of input reverse reads in FASTQ format.',required=True)

        parser.add_argument('-n', '--first_N_bases',
                            help='Remove all but a single representative of clusters of reads whose first [N]\
                            base pairs are identical. Default: 50, as recommended by MG-RAST. ',type=int,default=50)

        parser.add_argument('-o', '--output_prefix',
                            help='The prefix of de-replicated fastq files.',required=True)

       
        args = parser.parse_args()   
        
        f_iter = FastqGeneralIterator(safe_open(args.forward_reads_fp,"rb"))
        r_iter = FastqGeneralIterator(safe_open(args.reverse_reads_fp,"rb"))
        write1 = safe_open(args.output_prefix+'.de.1.fq', 'wb')
        write2 = safe_open(args.output_prefix+'.de.2.fq', 'wb')

        i, j = 0, 0
        a1, a2, i1, i2, j1, j2, j3 = {}, {}, 0, 0, 0, 0, 0

        start=time.time()
        wrerr = sys.stderr.write
        
        for (f_id, f_seq, f_qual), (r_id, r_seq, r_qual) in itertools.izip(f_iter,r_iter):
            i += 1
            i1 += 1
            i2 += 1
            
            if i%1000000==0:
                print i,'> PE reads scanned!'

            seq1 = str(f_seq)
            seq2 = str(r_seq)
            
            a1[seq1[0:args.first_N_bases]]=i1
            a2[seq2[0:args.first_N_bases]]=i2

            if len(a1) + j1 == i1 and len(a2) + j2 == i2:
                write1.write("@%s\n%s\n+\n%s\n" % (f_id, f_seq, f_qual))
                write2.write("@%s\n%s\n+\n%s\n" % (r_id, r_seq, r_qual))
                j += 1
            elif len(a1) + j1 != i1 and len(a2) + j2 == i2:
                j1 += 1
                continue
            elif len(a1) + j1 == i1 and len(a2) + j2 != i2:
                j2 += 1
                continue
            else:
                j1 += 1
                j2 += 1
                j3 += 1
                continue
                
        print str(j)+'/'+str(i),'PE reads written!'
        print j1-j3, 'replicate reads only in',args.forward_reads_fp
        print j2-j3, 'replicate reads only in',args.reverse_reads_fp
        print j3, 'replicate reads in both '+args.forward_reads_fp+' and '+args.reverse_reads_fp

        write1.close()
        write2.close()

        
        end=time.time()
        wrerr("OK, De-Replication finished in %3.2f secs\n" % (end-start))
