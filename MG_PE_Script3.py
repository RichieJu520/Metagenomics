"""
@author: Feng Ju
@email: richieju520@gmail.com
The script was written and tested in python 2.7 and biopython 1.58
"""

try:  
    from Bio import SeqIO
    from Bio.Seq import reverse_complement
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

if __name__ == '__main__':

        parser = argparse.ArgumentParser(description='a script for Overlapping Pair-End (PE) Reads <richieju520@gmail.com>')

        parser.add_argument('-f', '--forward_reads_fp',
                            help='The file path of input forward reads in FASTQ format.',required=True)

        parser.add_argument('-r', '--reverse_reads_fp',
                            help='The file path of input reverse reads in FASTQ format.',required=True)

        parser.add_argument('-j', '--min_overlap_len',
                            help='the minimum length (bp) for PE reads overlapping. Default: 10',type=int,default=10)

        parser.add_argument('-o', '--output_prefix',
                            help='The prefix of overlapped fasta file',required=True)

       
        args = parser.parse_args()   
        
        Format = 'fastq'
        
        handle1 = safe_open(args.forward_reads_fp, 'rb')
        handle2 = safe_open(args.reverse_reads_fp, 'rb')
        write1 = safe_open(args.output_prefix+'.mg.fasta', 'wb')
        
        SeqIO1 = SeqIO.parse(handle1, Format)
        SeqIO2 = SeqIO.parse(handle2, Format)
        
        i, j = 0, 0
        length_list = []

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
                
                seq1 = str(record1.seq)
                seq2 = str(record2.seq.reverse_complement())
                ReadID = str(record1.id)

                length = len(seq1)

                for k in range(length - args.min_overlap_len + 1):
                    if seq1[k:] == seq2[:(length-k)]:
                        j += 1
                        write1.write('>'+ReadID+'\n')
                        write1.write(seq1+seq2[(length-k):]+'\n')
                        length_list.append(len(seq1+seq2[(length-k):]))
                        break
                
        L_min = min(length_list)
        L_max = max(length_list)
        L_ave = "%.2lf" %(float(sum(length_list))/len(length_list))

        print 'In total, %d PE reads overlapped and %d itags are obtained' % (i, j)
        print 100*float(j)/i,'% tag yield ratio'
        print 'The length (bp) of the itags is between',L_min,'and',L_max,'with an average value at',L_ave
        

        write1.close()
        
        end=time.time()
        wrerr("OK, PE reads overlapping finished in %3.2f secs\n" % (end-start))
