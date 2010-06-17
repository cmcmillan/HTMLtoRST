#! /usr/bin/env python

import urllib2
import cleanup
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
