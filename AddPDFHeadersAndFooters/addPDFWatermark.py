#! /usr/bin/env python

from pyPdf import PdfFileWriter, PdfFileReader
from optparse import OptionParser
from datetime import datetime
import os
import makeHeaderWatermark

def main():
    parser = OptionParser()
    
    parser.add_option("-i", "--input-pdf", dest="sourcePDF",
        action = "store", metavar="PDF", 
        help="read the source PDF that will have the watermark and/or headers added")
    
    parser.add_option("-o", "--output-pdf", dest="outputPDFName",
        action = "store", metavar="FILE", 
        help="write the updated PDF to FILE. [default: source PDF file with a datestamp applied will be used.]")

    parser.add_option("-w", "--watermark-pdf", dest="watermarkPDFName", 
        action = "store", metavar="WATERMARK",
        help="optional WATERMARK pdf to be applied to each page of the input PDF. [default: %default]")
    
    parser.add_option("-c", "--classif" , "--classification", dest="classification", 
        action = "store", metavar="CLASSIFICATION",
        help="CLASSIFICATION of the PDF. [default: %default]", default="UNCLASSIFIED")
    
    parser.add_option("-c", "--classif" , "--classification", dest="classification", 
        action = "store", type="choice", choices = ( "", "UNCLASSIFIED" , "SECRET" ), metavar="CLASSIFICATION",
        help="CLASSIFICATION of the PDF. [default: %default]", default="UNCLASSIFIED")
    
    parser.add_option("-t", "--title" , dest="title", 
        action = "store", metavar="TITLE",
        help="TITLE of the PDF. [default: %default]", default="")
    
    parser.add_option("-h", "--header" , dest="header", 
        action = "store_true", default = True,
        help="add a header of the classification and title to PDF file, [default: %default]")
    
    parser.add_option("--no-header" , dest="header", 
        action = "store_false", 
        help="do not add a header of the classification and title to PDF file")
    
    parser.add_option("-f", "--footer" , dest="footer", 
        action = "store_true", default = True,
        help="add a footer of the classification and title to PDF file, [default: %default]")
    
    parser.add_option("--no-footer" , dest="footer", 
        action = "store_false", 
        help="do not add footer of the classification and title to PDF file")
    
    options, args = parser.parse_args()
    output = PdfFileWriter()
    
    if options.sourcePDF is None or 
        ( os.path.exists(options.sourcePDF) and not os.path.splitext(options.sourcePDF)[1].lower() == "pdf"):
        
        print "Source PDF Name is required and must exist."
        parser.print_version()
        parser.print_usage()
        parser.print_help()
        return
        
    sourcePDFName =os.path.splitext(options.sourcePDF)[0]
    timestamp = datetime.now()
    
    headerPDFName = "%s-header-%s" % (sourcePDFName, timestamp)
    if options.header is True or options.footer is True:
        # Make the Header Watermark PDF
        makeHeaderWatermark.makeWatermarkPdf(headerPDFName, 
        
    with open(options.sourcePDF, "rb") as sourcePDFFile:
        sourcePDF = PdfFileReader( sourcePDFFile )
        

