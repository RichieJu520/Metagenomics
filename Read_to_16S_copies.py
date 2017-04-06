from Bio import SeqIO

filename1 = "91_otus.fasta"  # 16S rRNA gene database used
filename2 = "W52_2.16s"   #blast output(format 6) from reads search against database
ReadLen = 150

RefLen = {}
for rec in SeqIO.parse(filename1, "fasta"):
    RefLen[str(rec.id)] = len(str(rec.seq))

N = len(RefLen)
print N, 'seqs in', filename1, 'with an average length of ', float(sum(RefLen.values()))/N, 'bp'
    
a = {}
b = {}
m, n = 0, 0
for line in open(filename2,'r'):
    m += 1
    lis = line.split('\t')
    try:
        b[lis[0]] = b[lis[0]] + 1  # Ignore repeated hits from the same query id
        n += 1
    except KeyError:
        b[lis[0]] = 1
        try:
            a[lis[1]] = a[lis[1]] + 1
        except KeyError:
            a[lis[1]] = 1

if n!=0:
    print n, 'repeated hits from the same query ignored!'
    
print (m-n), '16S rRNA gene reads in ', filename1

f = open(filename2+'_reads_to_copies.csv','w')
j = 0.0
for key in a.keys():
    copies = float(a[key]*ReadLen)/RefLen[key]
    j += copies
    f.write(key +',' + str(copies) + '\n')

print j, 'copies of 16S rRNA gene in ', filename1

print 'DONE!'
