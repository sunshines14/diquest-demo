import sys

num=1
outfile=open(sys.argv[2],'w')
with open(sys.argv[1],'r') as infile:
    for line in infile:
        text='uttr_%09d' % (num)
        outfile.write(text+" "+line)
        num=num+1

