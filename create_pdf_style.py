#! /usr/bin/env python

'''
create_pdf_style.py is a collection of functions for converting CSS styles
to reportlab.lib.styles 
'''

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet
from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2, sys, re
from copy import deepcopy

_soup = None
_url = "http://office.microsoft.com/en-us/sharepoint-server-help/use-a-collect-feedback-workflow-HA010154426.aspx?CTT=3"

def _getSoup():
    '''
    Get the backup soup
    '''
    if _soup is None:
        page = urllib2.urlopen(_url)
        _soup = BeautifulSoup(page)
    return deepcopy(_soup)

def getPrettyUrlContent(url):
    
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    
    return soup.prettify()

def getCssStyles(soup):
    
    if soup is None:
        soup = _getSoup()
        
    # Find tags where the href ends in ".css" or ".css" followed by "?" and some parameters 
    cssTags = soup.findAll(href=re.compile( r"(.+\.css^|.+\.css\?.+)" ) , rel="stylesheet")
    cssStyles = {}
    cssCounter = 1
    for cssTag in cssTags:
        styleName = None
        
        if cssTag["id"] is None:
            styleName = "style%s" % ( cssCounter ) 
            cssCounter + 1
        else:
            styleName = cssTag["id"]
            
        cssStyles.setdefault( styleName, getPrettyUrlContent( cssTag["href"] ) )
        print "cssTag['id']: %s" % ( cssTag["id"] )
        print "cssTag['href']: %s" % ( cssTag["href"] )
        print
    return cssStyles


    
def main():
    url = "http://office.microsoft.com/en-us/sharepoint-server-help/use-a-collect-feedback-workflow-HA010154426.aspx?CTT=3"
    
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    
    getCssStyles(soup)
    
    
if __name__ == "__main__":
    main()
