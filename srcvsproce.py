#!/usr/bin/env python
#encoding: utf-8

import csv
import re


if __name__=='__main__':

    pm = re.compile(r'[-|/][B|M|S]R\d+',re.U)
    
    with open('1415JRSR_SR.csv','wb') as fr: #'w',have blank row.
        fr_csv = csv.writer(fr)
    
        with open('1415JRSR.csv') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
            	rlset= set()
                rl = re.findall(pm,row[9])
                rlset = set(rl)
                rll = []
                for x in rlset:
                    rll.append(x)
                for ll in rll:
                    row.append(ll)
                    fr_csv.writerow(row)
                    row.pop()
    


