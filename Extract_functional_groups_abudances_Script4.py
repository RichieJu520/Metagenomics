filename=raw_input('Enter the name of matrix txtfile bearing taxon name and abudance: ')
filename2=raw_input('Enter the txt file of pathogen list: ')
f1=open(filename,'r')
f2=open(filename+'.count.csv','w')

i=0
a={}

for line in f1:
    a[line.split('\t')[0].strip()]=line.split('\t')[1].strip()

b=[]
for line in open(filename2,'r'):
    if line!='\n':
        b.append(line.strip())
print 'The functional list:'
print b

for item in b:
    if item in a.keys():
        f2.write(item+','+a[item]+'\n')
    else:
        f2.write(item+','+'0'+'\n')

print 'OK, finished'
raw_input('Press <Enter> to close this window!')

