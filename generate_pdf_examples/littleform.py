#! /usr/bin/env python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# By default the paper size is A4 so change it to letter size
c = canvas.Canvas("form.pdf", pagesize = letter)
c.setLineWidth(.3)
c.setFont('Helvetica', 12)

c.drawString(30, 750, 'OFFICAL COMMUNIQUE')
c.drawString(30, 735, ' OF ACME INDUSTRIES')
c.drawString(500, 750, '12/12/2010')
c.line(480, 747, 580, 747)

c.drawString(275, 725, 'AMOUNT OWED:')
c.drawString(500, 725, '$1,000.00')
c.line(378, 723, 580, 723)

c.drawString(30, 703, 'RECIEVED BY:')
c.line(120, 700, 580, 700)
c.drawString(120, 703, "JOHN DOE")

c.save()
