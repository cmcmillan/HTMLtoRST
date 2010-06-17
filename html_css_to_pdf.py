#! /usr/bin/env python

## {{{ http://code.activestate.com/recipes/572160/ (r1)
import cStringIO
import ho.pisa as pisa
import os

# Shortcut for dumping all logs on screen
pisa.showLogging()

def HTML2PDF(data, filename, openFile=False):

    """
    Simple test showing how to create a PDF file from
    PML Source String. Also shows errors and tries to start
    the resulting PDF
    """

    with open(filename,"wb") as pdfFile:
        pdf = pisa.CreatePDF(
                            cStringIO.StringIO(data),
                            pdfFile)
        pdfFile.flush()
        pdfFile.close()

    if openFile and (not pdf.err):
        os.startfile(str(filename))

    return not pdf.err



if __name__=="__main__":
    HTMLTEST = """
    <html><body>
    <p>Hello <strong style="color: #f00;">World</strong>
    <hr>
    <table border="1" style="background: #eee; padding: 0.5em;">
        <tr>
            <td>Amount</td>
            <td>Description</td>
            <td>Total</td>
        </tr>
        <tr>
            <td>1</td>
            <td>Good weather</td>
            <td>0 EUR</td>
        </tr>
        <tr style="font-weight: bold">
            <td colspan="2" align="right">Sum</td>
            <td>0 EUR</td>
        </tr>
    </table>
    </body></html>
    """

    HTML2PDF(HTMLTEST, "test.pdf", openFile=True)
## end of http://code.activestate.com/recipes/572160/ }}}

