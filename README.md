# These three scripts written for pretreatment of paired-end sequences for metagenomics

QC_PE.py  a script for Quality Control (QC) of Illumina Paired-End (PE) Reads.  

DR_PE.py  a script for De-Replication of Paired-End (PE) Reads.  

MG_PE.py  a script for Overlapping/Merging Paired-End (PE) Reads.  

The scripts were written and tested in python 2.7.3 and biopython 1.64


QC_PE.py -h
usage: QC_PE.py [-h] -f FORWARD_READS_FP -r REVERSE_READS_FP [-a MAX_AMBIG]
                [-L MIN_SEQ_LENGTH] [-q AVERAGE_QUALITY] [-F {33,64}] -o
                OUTPUT_PREFIX

a script for Quality Control (QC) of Illumina Paired-End (PE) Reads
<richieju520@gmail.com>

optional arguments:
  -h, --help            show this help message and exit
  -f FORWARD_READS_FP, --forward_reads_fp FORWARD_READS_FP
                        The file path of input forward reads in FASTQ format.
  -r REVERSE_READS_FP, --reverse_reads_fp REVERSE_READS_FP
                        The file path of input reverse reads in FASTQ format.
  -a MAX_AMBIG, --max_ambig MAX_AMBIG
                        maxmium number of ambiguous bases. Default: 3
  -L MIN_SEQ_LENGTH, --min_seq_length MIN_SEQ_LENGTH
                        minimum sequence length (bp). Default: 50
  -q AVERAGE_QUALITY, --average_quality AVERAGE_QUALITY
                        minimum average quality, Default: 20
  -F {33,64}, --phred_format {33,64}
                        format of phred quality score, Default: 33
  -o OUTPUT_PREFIX, --output_prefix OUTPUT_PREFIX
                        The prefix of filtered fastq files.


DR_PE.py -h
usage: DR_PE.py [-h] -f FORWARD_READS_FP -r REVERSE_READS_FP
                [-n FIRST_N_BASES] -o OUTPUT_PREFIX

a script for De-Replication of Paired-End (PE) Reads <richieju520@gmail.com>

optional arguments:
  -h, --help            show this help message and exit
  -f FORWARD_READS_FP, --forward_reads_fp FORWARD_READS_FP
                        The file path of input forward reads in FASTQ format.
  -r REVERSE_READS_FP, --reverse_reads_fp REVERSE_READS_FP
                        The file path of input reverse reads in FASTQ format.
  -n FIRST_N_BASES, --first_N_bases FIRST_N_BASES
                        Remove all but a single representative of clusters of
                        reads whose first [N] base pairs are identical.
                        Default: 50, as recommended by MG-RAST.
  -o OUTPUT_PREFIX, --output_prefix OUTPUT_PREFIX
                        The prefix of de-replicated fastq files.


MG_PE.py -h
usage: MG_PE.py [-h] -f FORWARD_READS_FP -r REVERSE_READS_FP
                [-j MIN_OVERLAP_LEN] -o OUTPUT_PREFIX

a script for Overlapping Paired-End (PE) Reads <richieju520@gmail.com>

optional arguments:
  -h, --help            show this help message and exit
  -f FORWARD_READS_FP, --forward_reads_fp FORWARD_READS_FP
                        The file path of input forward reads in FASTQ format.
  -r REVERSE_READS_FP, --reverse_reads_fp REVERSE_READS_FP
                        The file path of input reverse reads in FASTQ format.
  -j MIN_OVERLAP_LEN, --min_overlap_len MIN_OVERLAP_LEN
                        the minimum length (bp) for PE reads overlapping.
                        Default: 10
  -o OUTPUT_PREFIX, --output_prefix OUTPUT_PREFIX
                        The prefix of overlapped fasta file

