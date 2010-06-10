#! /usr/bin/env python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# By default the paper size is A4 so change it to letter size
c = canvas.Canvas("myfile.pdf", pagesize = letter)

# Grab the width and height to use later for calculations
# like when to add a page break or help define margins
width, height = letter
c.drawString(100, 750, "Welcome to Reportlab!")
c.save()
