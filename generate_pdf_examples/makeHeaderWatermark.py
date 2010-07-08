#! /usr/bin/env python

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen.textobject import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, red, blue, green
    
def getText(classification = None,  title = None, seperator = "--"):
    
    result = None
    
    if classification is None and title is None:
        result = None
    elif len(classification) > 0:
        classification = "%(seperator)s %(classif)s %(seperator)s" % { "seperator" : seperator , "classif" : classification.upper() }
        if title is not None and len(title) > 0:
            result = "%(classif)s %(title)s %(classif)s" % {"classif" : classification, "title" : title}
        else:
            result = classification
    elif len(title) > 0:
        result = classification = "%(seperator)s %(title)s %(seperator)s" % { "seperator" : seperator , "title" : title }
    
    return result
    
def makeWatermark(watermark, classification = "UNCLASSIFIED", title = None, header = True, footer = True, fontName = "Times-Bold", fontSize = 6):
    
    # Save the current state so it can be restored
    watermark.saveState()
    # Change the font, by default Times-Bold, size 6
    watermark.setFont(fontName, fontSize)
    width, height = watermark._pagesize
    ascent, descent = pdfmetrics.getAscentDescent(fontName, fontSize)
    centerX = width/2
    bottomY = abs(descent) * 2
    topY = height - (ascent*2)
    seperator = "--"
    
    if classification is not None:
        classification = classification.upper()
        if classification == "UNCLASSIFIED":
            watermark.setFillColor(green)
        elif classification == "SECRET":
            watermark.setFillColor(red)
        
    text = getText(classification, title, seperator)

    # Header
    if header is True:
        watermark.drawCentredString(centerX, topY, text)
    # Footer
    if footer is True:
        watermark.drawCentredString(centerX, bottomY, text)
        
    # Restore back to the state before we messed with colors and fonts
    watermark.restoreState()

def main():
    
    watermark = Canvas("watermark.pdf", pagesize=letter)
    makeWatermark(watermark, title = "The Business Data Catalog")
    watermark.save()
    
if __name__ == "__main__":
    main()
