#!/usr/bin/python

import sys
import os

hwufile=sys.argv[1]

plots = []

path = os.path.split(hwufile)[0]


for l in open(hwufile):
    if l.startswith('#') or not l.strip():
        continue
    if '<histogram>' in l:
        tags = l.split('"')[1].split('|')
        try:
            name = (tags[0].strip()+tags[3].strip()).replace(' ','_').replace('TYPE@#1','_').replace('/','o').replace('[','').replace(']','')
            #name = (tags[0].strip()+tags[-1].strip()).replace(' ','_').replace('TYPE@','').replace('T@','').replace('/','o').replace('[','').replace(']','')
        except IndexError:
            name = tags[0].strip().replace(' ','_').replace('TYPE@','').replace('/','o').replace('[','').replace(']','')
        name = name.strip()
        while name in plots:
            name=name+'_1'
#        print 'DOING', name
        thisplot = open(os.path.join(path, name+'.dat'), 'w')
        plots.append(name)
    elif '</histogram>' in l:
        thisplot.close()
    else:
        thisplot.write(l)
