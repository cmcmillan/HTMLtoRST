#! /usr/bin/env python

import urllib2
#import cleanup
from BeautifulSoup import BeautifulSoup
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet

def outputCssUrlSoup():
    url = r"http://officeimg.vo.msecnd.net/_layouts/ont.css?b=5512%2E3001"
    fileName = "css_ellipsis.css"
    css = urllib2.urlopen(url)
    # Write out the prettified version of the soup
    with open( fileName , "wb") as soupOutput:
        soupOutput.write(css.read())
        soupOutput.flush()
        soupOutput.close()

def platypusHtml2Pdf(url, fileName, openFile=False):
    
    style = getSampleStyleSheet()
    pdf = SimpleDocTemplate(fileName, pagesize=letter)
    
    html = page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    para = Paragraph(soup.prettify(), style["Normal"])
    story.append(para)
    
    pdf.build(story)
    
    if openFile:
        os.startfile( str( fileName ) )
        
def main():
    url = "http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html"
    pdfName = "platypusHTML2PDF.pdf"
    platypusHtml2Pdf(url, pdfName, True)
    
if __name__=="__main__":
    main()
