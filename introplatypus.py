from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet
from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2, sys, re

style = getSampleStyleSheet()
pdf = SimpleDocTemplate("testplatypus3.pdf", pagesize=letter)
story = []
text = "Paragraphs are quite ease to create with Platypus, and Platypus handles\
     things like word wrapping for you. There's not a lot of coding work involved if\
     you wish to create something simple."

print
print "byName"
print
styleNames = style.byName

for styleName in styleNames:
    para = Paragraph("Style Name: %s" % (styleName), style[styleName])
    print styleName
    story.append(para)
    story.append(Spacer(inch*0.5,inch*0.5))

print
print "byAlias"
print
aliasNames = sorted(style.byAlias)

for alias in aliasNames:
    para = Paragraph("Alias: %s" % (alias), style[alias])
    print alias
    story.append(para)
    story.append(Spacer(inch*0.5,inch*0.5))

for x in xrange(25):
    para = Paragraph(text, style["Normal"])
    story.append(para)
    story.append(Spacer(inch*0.5,inch*0.5))

for color in ["red","green","blue"]:
    para = Paragraph("<font color='%s'>This is <b>%s</b>.</font>" % (color,color), style["Normal"])
    story.append(para)
    story.append(Spacer(inch*0.5, inch*0.5))

#story.append(Image("http://images.devshed.com/ds/stories/PyPDF/devshed.jpg"))

#address = sys.argv[1]
address = "http://www.mono-project.com/Gendarme.Rules.BadPractice"
html = url = urllib2.urlopen(address).read()
soup = BeautifulSoup(html)
story.append(soup.prettify())
#print type(content)
#print content.renderContents()

#story.append(content)

#pdf.build()
pdf.build(story)
