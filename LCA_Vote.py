import operator
import sys

sys.argv1 = "Rep-OTU-ID-refseq-95hits.ublast.annotated.taxa.path.txt" #Map file with ReadName to TaxaPath from MEGAN
sys.argv2 = "0.5"         #Minimum percentage to vote for LCA

d = {}
sys.argv2 = float(sys.argv2)
for line in open(sys.argv1,'r'):
    lis = line.strip().split(',')
    ID = '_'.join(lis[0].split('_')[:2])
    lis1 = lis[1].strip().split(';')
    try:
        d[ID].append(lis1)
    except KeyError:
        d[ID] = [lis1]
print len(d), 'contigs!'

f=open(sys.argv1+'_LCA_'+str(sys.argv2)+'.csv','w')
k = 0
for key in d.keys():
    k+=1
    lis1 = d[key]
    N1 = len(lis1)
    taxa = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    #print N1, 'ORFs on the contigs!'
    for ORF in lis1:
        for i in range(len(ORF)):
            taxa[i].append(';'.join(ORF[:i]))
    dic = {}
    for j in range(len(taxa)):
        d1 = {}
        item = taxa[j]
        item1 = list(set(item))
        for i in item:
            d1[i]= item.count(i)
        sorted_d1 = sorted(d1.items(), key=operator.itemgetter(1))
        try:
            LCA = sorted_d1[-1][0]
            N2  = sorted_d1[-1][1]
            if float(N2)/N1 >= sys.argv2:
                dic[j] = [LCA, N2]
                continue
            else:
                LCA = dic[j-1][0]
                N2  = dic[j-1][1]
                break
        except IndexError:
            break
    f.write(','.join([key, str(N1), str(N2), LCA])+'\n')
            
print 'DONE!'
