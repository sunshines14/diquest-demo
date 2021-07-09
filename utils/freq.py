from konlpy.tag import Okt
from collections import Counter
import sys

inputfile = sys.argv[1]
outputfile = sys.argv[2]
threshold = 1000
with open(inputfile, "r") as f:
    lines = f.read()
    nlpy = Okt()
    nouns = nlpy.nouns(lines)
    #print(nouns)
    
    count = Counter(nouns)
    tag_count = []
    tags = []
    for n, c in count.most_common(threshold):
        dics = {'tag': n, 'count': c}
        if len(dics['tag']) >= 2:
            tag_count.append(dics)
            tags.append(dics['tag'])
    for tag in tag_count:
        print("{}".format(tag['tag']), end='\t')
        print("{}".format(tag['count']))
    print (len(nouns))

with open(outputfile, "w") as f:
    for tag in tag_count:
        f.write(str(tag['tag'])+'\t'+str(tag['count']))
        f.write('\n')
