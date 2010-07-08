#! /usr/bin/env python

import urllib2
import cleanup
from stoneagepdf import CompactifyingSoup
from docutils.parsers import rst
from BeautifulSoup import BeautifulSoup
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet
'''
	Print a nice clean PDF file from a website URL.
	Optionally merge the new result PDF result into another PDF,
	updating the table of contents of both documents.

	Step 1) Clean up the HTML/CSS
	Step 2) Convert Clean HTML/CSS to PDF
'''
def printValue( varName, varVal , indentLevel = 0, indentChar = "    ",
                valueIndentLevel = 0, valueIndentChar = " ", valueSeperator = ":"):
    '''
    Prints out the value of a variable in one of the formats:

        "Indentation" +  "varName" + "seperator" + "ValueIndentation" +  "varValue"

    or if "ValueIndentation" contains a new line character

        "Indentation" +  "varName" + "seperator" + "ValueIndentation" +  "Indentation" + "varValue"

    where the "indentLevel" and "valueIndentLevel" determine the occurrences of "indentChar" and "valueIndentChar"
    '''

    indentation = ""
    valueIndentation = " "

    # Fix any of the indentation levels if they are negative
    if indentLevel < 0:
        indentLevel = 0
    if valueIndentLevel < 0:
        valueIndentLevel = 0

    if indentLevel > 0:
        indentation = str(indentChar) * indentLevel
    if valueIndentLevel > 0:
        valueIndentation = str(valueIndentChar) * valueIndentLevel

        if valueIndentation.count("\n") > 0:
            # There is at least one new line so append the starting indentation as well
            valueIndentation = valueIndentation + indentation

    print "%(indent)s%(name)s%(seperator)s%(valueIndent)s%(value)s" % \
        {
            "indent" : indentation ,
            "name" : varName ,
            "seperator" : valueSeperator ,
            "valueIndent" : valueIndentation ,
            "value" : varVal
        }


def saveSoupLines(soupLines, fileName=None):
    '''
    Save a Beautiful Soup to a file using prettify.
    If fileName is None, no file is written and just the prettify Beautiful Soup is returned
    '''
    validOutput = False
    if fileName is not None:

        # Write out the prettified version of the soup
        with open( fileName , "wb") as soupOutput:
            soupOutput.write(soupLines)
            soupOutput.flush()
            soupOutput.close()

        # Read the file back in so that we can return the results
        with open( fileName , "rb" ) as soupInput:
            validOuput = soupLines == soupInput.read()
            soupInput.close

    return validOutput

def SimplifyURL(url):
    
    page = urllib2.urlopen(url)
    stoneageSoup = CompactifyingSoup(page)
    
    printValue( "stoneageSoup.compactify()", 
        saveSoupLines( stoneageSoup.compactify() , "output/simpleCompactSoup.html") )
    
    printValue( "stoneageSoup.compactify(remove_classnames_and_ids=True)", 
        saveSoupLines( stoneageSoup.compactify(remove_classnames_and_ids=True) , "output/noClassNamesAndIDsCompactSoup.html") )
    
if __name__=="__main__":
    SimplifyURL("http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html")
