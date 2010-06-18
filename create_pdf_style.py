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
import urllib2, sys, re, os
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

def getSoup(url):
    
    print "URL: %s" % url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    
    return soup

def getPrettyUrlContent(url):
    
    soup = getSoup(url)
    
    return soup.prettify()

def getCssStyles(url):
    
    soup = getSoup(url)
        
    # Find tags where the href ends in ".css" or ".css" followed by "?" and some parameters 
    cssTags = soup.findAll(href=re.compile( r"(.+\.css$|.+\.css\?.+)" ) , rel="stylesheet")
    #cssTags = soup.findAll(href=re.compile( r".+\.css$" ) , rel="stylesheet")
    print len(cssTags)
    cssStyles = {}
    cssCounter = 1
    baseURL = os.path.split(url)[0] + "/"
    for cssTag in cssTags:
        styleName = None
        
        if cssTag.has_key("id") is False:
            cssTag["id"] = "style%s" % ( cssCounter ) 
            cssCounter + 1
        
        styleName = cssTag["id"]
        
        if cssTag["href"].startswith("http") is False:
            cssTag["href"] = baseURL + cssTag["href"]
        
        cssStyles.setdefault( styleName, getPrettyUrlContent( cssTag["href"] ) )
        
        print "cssTag['id']: %s" % ( cssTag["id"] )
        print "cssTag['href']: %s" % ( cssTag["href"] )
        print
    return cssStyles

def getMasterCssStyle(cssStyles):
    masterCss = []
    for cssStyleName, cssStyle in  cssStyles.iteritems():
        masterCss.append(cssStyle)
    return "\n".join(masterCss)
    
def saveToFile(data, pathName):
    with open(pathName , "wb") as dataFile:
            dataFile.write(data)
            dataFile.flush()
            dataFile.close()

def saveCssStyles(cssStyles, path):
    for cssStyleName, cssStyle in  cssStyles.iteritems():
        
        saveToFile(cssStyle, os.path.join(path, "%s.css" % (cssStyleName) ))

def getPdfStyles(cssStyles):
    
    pdfStyles = {}
    
    for cssStyleName, cssStyle in  cssStyles.iteritems():
        pdfStyle = getSampleStyleSheet()
        pdf

def getRulesForElement(soup, masterCSS, name, attrName):
    
    from repoze.cssutils import css
    cssParser = css.CSSParser()
    stylesheets = cssParser.parse(masterCSS)
    
    element = soup.find(name, attrName)
    
    rules = myCssParser.parse(cssData).findAllCSSRulesFor(element)
    for rule in rules:
        print rule
        
    
def main():
    url = "http://office.microsoft.com/en-us/sharepoint-server-help/use-a-collect-feedback-workflow-HA010154426.aspx?CTT=3"
    url = "http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html"
    # page = urllib2.urlopen(url)
    # soup = BeautifulSoup(page)
    
    cssStyles = getCssStyles(url)
    #saveCssStyles(cssStyles,"")
    masterCss = getMasterCssStyle(cssStyles)
    saveToFile(masterCss, "main_reStructuredText.css")
    getRulesForElement(getSoup(url), masterCss
    
    
if __name__ == "__main__":
    main()
    #print os.path.split("http://www.media.com/teledha/TV/s")
    #print os.path.join("http://www.media.com/teledha/TV/s","../../look")
