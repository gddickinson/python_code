# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 19:50:08 2017

@author: George
"""

#==============================================================================
# import os
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfparser import PDFDocument
# 
# #fp = open("foo.pdf", 'rb')
# fp = open(r'C:\Users\George\Desktop\report_no_dir\abiotic_factors_insect_pop_07.pdf', 'rb')
# 
# parser = PDFParser(fp)
# doc = PDFDocument(parser)
# parser.set_document(doc)
# doc.set_parser(parser)
# if len(doc.info) > 0:
#     info = doc.info[0]
#     print(info)
#==============================================================================


from PyPDF2 import PdfFileReader
pdf_toread = PdfFileReader(open(r'C:\Users\George\Dropbox\SoundScience\LCR_webpages\report_no_dir\abiotic_factors_insect_pop_07.pdf', "rb"))
pdf_info = pdf_toread.getDocumentInfo()
print (str(pdf_info))