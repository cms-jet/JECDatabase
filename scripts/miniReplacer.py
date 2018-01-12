#!/usr/bin/python

import sys

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    print("will replace\n",lines[line_num],"\n by\n",text)
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

newLine= "{ 1 JetEta 1 JetPt [2]*([3]*([4]+[5]*TMath::Log(max([0],min([1],x))))*1./([6]+[7]*100./3.*(TMath::Max(0.,1.03091-0.051154*pow(x,-0.154227))-TMath::Max(0.,1.03091-0.051154*TMath::Power(208.,-0.154227)))+[8]*0.021*(-1.+1./(1.+exp(-(TMath::Log(x)-5.030)/0.395))))) Correction L2Relative}\n"

print("will call replace_line(",sys.argv[1],",0,",newLine,")")
replace_line(sys.argv[1] , 0, newLine)



