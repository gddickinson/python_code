# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:11:09 2018

@author: George
"""
from __future__ import print_function
import sys, getopt, re


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('searchText_commLine.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('searchText_commLine.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    try:
        searchFile = open(inputfile, "r")
        text = searchFile.read()
        searchFile.close()
    except:
        print('Unable to open input file')
    
    #find all occurences of text within parentheses
    result = re.findall('\(.*?\)',text)
    
    result2 = re.findall(r'(.*?)\(.*?\)',text)
    
    result3 = []
    
    for i in range(len(result)):
        if re.search('\d+',result[i]) and len(result[i]) > 4:
            result[i] = result[i].encode('ascii', 'replace').decode('ascii')
            result2[i] = result2[i].encode('ascii', 'replace').decode('ascii')
            try:
                result3.append([result2[i][-30:],result[i]])
            except:
                result3.append([result2[i],result[i]])
    
    try:
        saveFile = open(outputfile, 'w')
         
        for item in result3:
            print(*item,file=saveFile, sep=',')
        
        saveFile.close()
    except:
        print('Unable to write results file')

if __name__ == "__main__":
   main(sys.argv[1:])