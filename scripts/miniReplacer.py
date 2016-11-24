#!/usr/bin/python

import sys

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

newLine= "{ 1 JetEta 1 JetPt [2]*([3]*([4]+[5]*TMath::Log(max([0],min([1],x))))*1./([6]+[7]*100./3.*(TMath::Max(0.,1.03091-0.051154*pow(x,-0.154227))-TMath::Max(0.,1.03091-0.051154*TMath::Power(208.,-0.154227)))+[8]*(-0.978049+(1+0.04432-1.304*pow(max(30.,min(6500.,x)),-0.4624)+(0+1.724*TMath::Log(max(30.,min(6500.,x))))/max(30.,min(6500.,x)))))) Correction L2Relative}\n"

print "will call replace_line(",sys.argv[1],",0,",newLine,")"
#replace_line(sys.argv[1] , 0, newLine)



