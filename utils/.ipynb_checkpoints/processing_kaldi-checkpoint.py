import re
import sys

referencefile = sys.argv[1]
kaldifile = sys.argv[2]
vadfile = sys.argv[3]
outputfile = sys.argv[4]
key = []
result = []

with open(referencefile, 'r') as f:
    flist = f.readlines()
    for i in range(len(flist)):
        flist_splited = flist[i].split(' ')
        key.append(flist_splited[0])

with open(kaldifile, 'r') as f:
    flist = f.readlines()
    for i in range(len(flist)):
        flist_splited = flist[i].split(' ')
        for j in range(len(key)):
            if flist_splited[0] in key[j]:
                result.append(flist[i][15:])
            else:
                continue

with open(outputfile, 'w') as wf:
    wf.write('onset'+','+'offset'+','+'result')
    wf.write('\n')
    with open(vadfile, 'r') as rf:
        flist = rf.readlines()
        for i in range(len(flist)):
            flist_splited = flist[i].split(',')
            tmp = result[i].replace('\n','').replace(' ▁','\t').replace(' ','').replace('\t',' ').replace('▁','')
            wf.write(flist_splited[0]+','+flist_splited[1]+','+tmp)
            wf.write('\n')
            print(flist_splited[0],flist_splited[1],tmp)