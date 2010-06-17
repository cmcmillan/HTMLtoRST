#! /usr/bin/env python

'''
Cleanup.py cleans up an HTML/CSS document to a santized XHTML document
'''

from BeautifulSoup import BeautifulSoup             # For processing HTML
from BeautifulSoup import BeautifulStoneSoup    # For processing XML
#import BeautifulSoup                                           # To get everything
import re                                                                # For Regular Expressions
import urllib2                                                         # For opening URLs
import os                                                                # For checking if file exists 


import cStringIO
import ho.pisa as pisa

# Reportlab PDF generation
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet

def htmlToPlatypus( data , pdfFileName, openFile=False):

    style = getSampleStyleSheet()
    pdf = SimpleDocTemplate(pdfFileName, pagesize=letter)

    story = []

    para = Paragraph(data, style["Normal"])
    story.append(para)

    pdf.build(story)

    if openFile is True:
        os.startfile( str( fileName ) )


def HTML2PDF(data, fileName, openFile=False):
    """
    Simple test showing how to create a PDF file from
    PML Source String. Also shows errors and tries to start
    the resulting PDF
    """

    # Shortcut for dumping all logs on screen
    pisa.showLogging()

    with open(fileName,"wb") as pdfFile:
        pdf = pisa.CreatePDF(
                            cStringIO.StringIO(data),
                            pdfFile)
        pdfFile.flush()
        pdfFile.close()

    if openFile and ( not pdf.err ):
        #os.startfile( str( fileName ) )
        pisa.startViewer( str( fileName ) )

    return not pdf.err

def extractAllTags(root, name=None, attrs = {}, recursive=True, text=None, limit=None, **kwargs):
    '''
    Extract all the tags that are found under root which can be either a soup or a sub Tag element
    '''

    for tag in root.findAll(name, attrs, recursive, text, limit, **kwargs):
        tag.extract()

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


def getCssStyleSheets(soup):
    

def manipulateSoup(soup, *args):
    '''    
    Perfom the provided Soup Manipulations
    '''
    
    for soupManipulation in args:
        soupManipulation( soup )

def outputSoup( soup , fileName=None , *soupManipulationArgs ):

    # Perfom any Soup Manipulations
    manipulateSoup(soup, *soupManipulationArgs)

    # Write out the soup
    return saveSoup( soup , fileName )

def outputSoupPDF(soup, pdfFileName , soupFileName = None , openFile=False, *soupManipulationArgs ):

    # Append Soup Manipulation task to remove the DOCTYPE since the PDF builder does not like it.
    soupManipulations = list(soupManipulationArgs)
    soupManipulations.append( lambda (soup) : 
                                                    extractAllTags(soup, text=re.compile("^DOCTYPE html*") ) )
    soupManipulationArgs = tuple(soupManipulations)
    
    processedSoup = outputSoup( soup , soupFileName, *soupManipulationArgs)

    #HTML2PDF( processedSoup , pdfFileName, openFile )
    htmlToPlatypus( processedSoup , pdfFileName, openFile )

def saveSoup(soup, fileName=None):
    '''
    Save a Beautiful Soup to a file using prettify.
    If fileName is None, no file is written and just the prettify Beautiful Soup is returned
    '''
    # Lines of soup that were actually written out
    soupLines = None

    if fileName is None:
        # return the prettify output
        soupLines = soup.prettify()

    else:
        # Write out the prettified version of the soup
        with open( fileName , "wb") as soupOutput:
            soupOutput.write(soup.prettify())
            soupOutput.flush()
            soupOutput.close()

        # Read the file back in so that we can return the results
        with open( fileName , "rb" ) as soupInput:
            soupLines = soupInput.read()
            soupInput.close

    return soupLines



def getBasicSoup():
    '''
    Get Beautiful Soup from a basic canned well formed HTML page
    '''
    doc = [ '<html><head><title>Page title</title></head>',
            '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
            '<p id="secondpara" align="blah">This is paragraph <b>two</b>.',
    '</html>']

    soup = BeautifulSoup( "".join( doc ) )
    return soup

def getBigSoup():
    '''
    Get Beautiful Soup from a big hunk of HTML code
    '''
    doc = """<div id="cdnavcontbck">

                            <!--BUILD VER: 14.0.5512.3001--><!--LLCC: en-US--><!--MACHINE: BLUREN105--><!--CORRELATIONID: abc6434a-b3d2-4ee8-9f2b-334155737920--><div id="cdnavcontainer">
                    <div id="cdtopnavlinks">
                <a class="cdchrm" rel="nofollow" href="http://login.live.com/login.srf?wa=wsignin1.0&amp;rpsnv=11&amp;ct=1276787501&amp;rver=5.5.4177.0&amp;wp=MBI&amp;wreply=http:%2F%2Foffice.microsoft.com%2Fwlid%2Fauthredir.aspx%3Furl%3D%252Fen%252Dus%252Fsharepoint%252Dserver%252Dhelp%252Fuse%252Da%252Dcollect%252Dfeedback%252Dworkflow%252DHA010154426%252Easpx%253FCTT%253D3%26hurl%3DE451F8876272C95A24EC8B39D648E448&amp;lc=1033&amp;id=34134" accesskey="2">Sign In</a><script type="text/javascript">var g_fSignedIn=false;</script>      <span> | </span><a class="cdglobe cdchrm" href="http://office.microsoft.com/en-us/worldwide.aspx?CTT=155" tabindex="-1"><img src="http://officeimg.vo.msecnd.net/_layouts/images/general/globe.png?b=5512%2E3001" alt="Click here to use Office.com in another language"></a><a class="cdchrm" href="http://office.microsoft.com/en-us/worldwide.aspx?CTT=155">United States</a>
                    </div><div class="cdclr">
                        &nbsp;

                    </div><div id="cdlogo">
                        <a href="http://office.microsoft.com/en-us/?CTT=97"><img src="http://officeimg.vo.msecnd.net/_layouts/images/general/office_logo.jpg?b=5512%2E3001" alt="Office.com" title="Office.com"></a>
                    </div><div id="cdskiptomain">
                        <a accesskey="4" href="#cdmainc">Skip to main content</a>
                    </div><form method="get" action="http://office.microsoft.com/en-us/sharepoint-server-help/results.aspx" id="frmSearch" class="cdfullsrchctrl" autocomplete="off">
                    <div class="cdmostborders cdbottomborder">
                        <input class="cdsrchtxt cdsrchdef" name="qu" value="" maxlength="128" id="qu" accesskey="3" title="Search for" type="text"><button type="submit" class="cdsrchbtn" value="" title="Click to search" alt="Click to search"><img src="http://officeimg.vo.msecnd.net/_layouts/images/general/search_button.png?b=5512%2E3001" title="Click to search" alt="Click to search"></button><input name="origin" value="HA010154426" type="hidden"><span>Search all of Office.com</span>
                    </div>

                </form><img src="http://officeimg.vo.msecnd.net/_layouts/images/general/bing.png?b=5512%2E3001" id="cdbinglogo" alt="Powered by Bing"><div id="cdtopnavpromo">
                        <div class="basiccontent_nb">
                  <table class="cntbasicTable" cellpadding="0" cellspacing="0">
                    <tbody><tr>
                      <td>
                        <div class="cntHCMBlurb"></div>
                      </td>
                      <td>
                        <div class="cntHCMBlurb"><a name="{&quot;la&quot;:&quot;XT101859253&quot;}" class="cdOOHomepageWpLinkMetrics" href="redir/XT101859253.aspx"><img src="http://officeimg.vo.msecnd.net/en-us/files/533/598/ZA101880355.png" alt="Find commands on the Office Ribbon: (c) Microsoft" title="Find commands on the Office Ribbon: (c) Microsoft" class="cnt10mr" align="left" border="0"></a></div>

                      </td>
                    </tr>
                  </tbody></table>
                  <div class="cntHCMListTitle"></div>
                </div>
                    </div><div class="cdclr">
                        &nbsp;
                    </div>
                </div>
                            <div id="cdtabarea">

                    <ul id="cdtoptabs">
                        <li class="cdtopn"><a href="http://office.microsoft.com/en-us/?CTT=97" accesskey="1">home</a></li><li class="cdtopn"><a href="http://office.microsoft.com/en-us/products/?CTT=97">products</a></li><li class="cdtopn cdselected"><a href="http://office.microsoft.com/en-us/support/?CTT=97">support</a></li><li class="cdtopn"><a href="http://office.microsoft.com/en-us/images/?CTT=97">images</a></li><li class="cdtopn"><a href="http://office.microsoft.com/en-us/templates/?CTT=97">templates</a></li><li class="cdtopn"><a href="http://office.microsoft.com/en-us/downloads/?CTT=97">downloads</a></li><li class="cdtopn cdhzmore cdtbhlder"><a href="http://office.microsoft.com/en-us/secmenu.aspx?origin=TN100982051" tabindex="-1">more</a><img src="http://officeimg.vo.msecnd.net/_layouts/images/general/more_arrow.png?b=5512%2E3001" alt=""><ul style="top: -5000px; left: 715.5px;" class="cdsectabs">
                            <li class="cdsecn"><a href="http://office.microsoft.com/en-us/office-site-directory-FX101808679.aspx?CTT=97">All Office.com</a></li><li class="cdsecn"><a href="http://office.microsoft.com/en-us/career-center-for-job-seekers-powered-by-monster-com-FX010350405.aspx?CTT=97">Career Center</a></li><li class="cdsecn"><a href="http://office.microsoft.com/en-us/redir/XT101785424.aspx?CTT=97">Office Labs</a></li><li class="cdsecn"><a href="http://office.microsoft.com/en-us/redir/XT101794943.aspx?CTT=97">Office for Mac</a></li><li class="cdsecn"><a href="http://office.microsoft.com/en-us/redir/XT101794946.aspx?CTT=97">Office for IT Pros</a></li><li class="cdsecn"><a href="http://office.microsoft.com/en-us/redir/XT101794947.aspx?CTT=97">Office for Developers</a></li><li class="cdsecn"><a href="http://office.microsoft.com/en-us/redir/XT101822759.aspx?CTT=97">All Microsoft Sites</a></li>

                        <li class="cdsecn cdsecnlast"><span>&nbsp;</span></li></ul></li><li class="cdclr">&nbsp;</li>
                    </ul>
                </div>

                    </div>"""

    soup = BeautifulSoup(doc)
    return soup

def getMegaSoup():
    '''
    Get Beautiful Soup from a mega hunk of HTML code
    '''
    doc = """<div class="cdArticleWrapper"><div class="cdArticle"><div class="cdArticleHead"><h1 class="cdTitleEx">Use a Collect Feedback workflow</h1><p class="cdAppliesToEx"><span class="cdAppliesToExLabel">Applies to: </span> <a href="http://office.microsoft.com/en-us/sharepoint-server-help/redir/FX010121172.aspx">Microsoft Office SharePoint Server 2007</a></p></div><div id="dvActionBar" class="dvActionBar"><span class="dvABLeftEdge"></span><span style="width: 611px;" class="dvABCenter"><span style="width: 0px;" class="dvActionBarLeft"></span><span style="width: 611px;" class="dvActionBarFull"><a class="ancABItem cdEllipsis" style="max-width: 589px;" title="Print" id="ancABRight0" href="javascript:void(0)">Print</a></span></span><span class="dvABRightEdge"></span></div><div class="cdArticleLeft"><div style="height: 297px;" class="cdArticleLeftMargin"><div class="cdArticleLeftMarginItems"></div><div class="cdclr">&nbsp;</div></div><div class="cdArticleBody"><div class="cdArticleText cntArticleBody"><div style="min-width: 81px;" class="cdExpandoLink" id="divShowAll"><a href="javascript:AlterAllDivs('block');" class="DropDown"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/785/945/ZA079005000.gif" alt="Show All" title="Show All" border="0">Show All</a></div>
                    <div style="display: none; min-width: 81px;" class="cdExpandoLink" id="divHideAll"><a href="javascript:AlterAllDivs('none');" class="DropDown"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/218/224/ZA079005001.gif" alt="Hide All" title="Hide All" border="0">Hide All</a></div>

                    <p><a name="BMbacktotop" id="BMbacktotop"></a>The Collect Feedback workflow routes a document or item that is saved to a list or library to a group of people to collect their review feedback. By default, the Collect Feedback workflow is associated with the Document content type and it is thus automatically available in document libraries.</p>
                    <div class="bmkTOChead"> </div>
                    <hr class="bmktocrule">
                    <ul id="bmkTOClist">

                      <li id="bmkTOClinks"><a href="#BM1">How does the Collect Feedback workflow work?</a></li>
                      <li id="bmkTOClinks"><a href="#BM2">Add or change a Collect Feedback workflow for a list, library, or content type</a></li>
                      <li id="bmkTOClinks"><a href="#BM3">Start a Collect Feedback workflow on a document or item</a></li>
                      <li id="bmkTOClinks"><a href="#BM4">Complete a Collect Feedback workflow task</a></li>
                    </ul>
                    <hr class="bmktocrule"><a id="BM1" name="BM1"></a><h2><a name="BM1" id="BM1"></a>How does the Collect Feedback workflow work?</h2>
                    <p>The Collect Feedback workflow supports business processes that involve sending a document or item to a group of people to collect review feedback. The Collect Feedback workflow makes a review business process more efficient by managing and tracking all of the human tasks involved with the process. After it is completed, the Collect Feedback workflow consolidates all of the feedback from reviewers for the workflow owner and it provides record of the review process.</p>

                    <p>If workflows are available, you can start a Collect Feedback workflow directly from a document or item in a list or library. To start a workflow, you select the workflow that you want to use, and then you fill out a workflow initiation form that specifies the workflow participants (reviewers), a due date, and any relevant task instructions. After a workflow starts, the server assigns tasks to all participants. If e-mail alerts are enabled for the server, the server also sends e-mail alerts to all participants . Participants can click a link in the e-mail task alert to open the document or item to be reviewed. Participants can make changes or insert comments directly in the document. In the task form, they can provide feedback comments. They can also reassign their review tasks or request a change to the document or item to be reviewed. Participants have the option of completing their workflow tasks from either the Microsoft Office SharePoint Server 2007 Web site or from directly within certain programs that are part of the 2007 Microsoft Office system. While the workflow is in progress, the workflow owner or the workflow participants can view the Workflow Status page to see which participants have completed their workflow tasks. When the workflow participants complete their workflow tasks, the workflow ends, and the workflow owner is automatically notified that the workflow is complete.</p>
                    <p>By default, the Collect Feedback workflow is associated with the Document content type and it is thus automatically available in document libraries. The default Collect Feedback workflow for document libraries is a parallel workflow in which tasks are assigned to all participants at the same time. You can customize this preassociated version of the Collect Feedback workflow to meet the needs of your organization, or you can add a completely new version of the Collect Feedback workflow to a list, library, or content type.</p>
                    <p><a href="#top"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/206/661/ZA010077668.gif" alt="Top of Page" title="Top of Page" border="0"></a> <a href="#top" class="cntTopOfPage">Top of Page</a></p><a id="BM2" name="BM2"></a><h2><a name="BM2" id="BM2"></a>Add or change a Collect Feedback workflow for a list, library, or content type</h2>
                    <p>Before a workflow can be used, it must be added to a list, library, or content type to make it available for documents or items in a specific location. You must have the Manage Lists permission to add a workflow to a list, library, or content type. In most cases, site administrators or individuals who manage specific lists or libraries perform this task.</p>
                    <p>The availability of a workflow within a site varies, depending on where it is added:</p>
                    <ul class="cntIndent36" type="disc">
                      <li>If you add a workflow directly to a list or library, it is available only for items in that list or library.</li>
                      <li>If you add a workflow to a list content type (an instance of a site content type that was added to a specific list or library), it is available only for items of that content type in the specific list or library with which that content type is associated.</li>

                      <li>If you add a workflow to a site content type, that workflow is available for any items of that content type in every list and library to which an instance of that site content type was added. If you want a workflow to be widely available across lists or libraries in a site collection for items of a specific content type, the most efficient way to achieve this result is by adding that workflow directly to a site content type.</li>
                    </ul>
                    <h3>Add or change a Collect Feedback workflow for a list, library, or content type</h3>
                    <p>If you want to add a Collect Feedback workflow to a list, library, or content type, or if you want to change a Collect Feedback workflow that is already associated with a list, library, or content type, you follow the same steps.</p>
                    <p>To open the Add a Workflow page or the Change a Workflow page for the list, library, or content type for which you want to add or change a workflow, do one of the following:</p>
                    <ul class="cntIndent36" type="disc">
                      <li>For a list or library:</li>
                      <ul type="disc">
                        <li>Open the list or library for which you want to add or change a workflow.</li>

                        <li>On the <b class="ui">Settings</b> menu <img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/346/344/ZA010095136.gif" alt="Settings menu" title="Settings menu" border="0">, click <b class="ui">List Settings</b>, or click the settings for the type of library that you are opening.</li>
                      </ul>
                    </ul>
                    <p class="cntIndent72">For example, in a document library, click <b class="ui">Document Library Settings</b>.</p>
                    <ul class="cntIndent72" type="disc">

                      <li>Under <b class="ui">Permissions and Management</b>, click <b class="ui">Workflow settings</b>.</li>
                    </ul>
                    <ul class="cntIndent36" type="disc">
                      <li>For a list content type: </li>
                    </ul>
                    <ul class="cntIndent72" type="disc">
                      <li>Open the list or library that contains the instance of the list content type for which you want to add or change a workflow.</li>

                      <li>On the <b class="ui">Settings</b> menu <img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/346/344/ZA010095136.gif" alt="Settings menu" title="Settings menu" border="0">, click <b class="ui">List Settings</b>, or click the settings for the type of library that you are opening.</li>
                    </ul>
                    <p class="cntIndent72">For example, in a document library, click <b class="ui">Document Library Settings</b>.</p>
                    <ul class="cntIndent72" type="disc">
                      <li>Under <b class="ui">Content Types</b>, click the name of the content type. </li>

                    </ul>
                    <p class="cntIndent72"><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;If the list or library is not set up to allow multiple content types, the <b class="ui">Content Types</b> section does not appear on the <b class="ui">Customize</b> page for the list or library.</p>
                    <ul class="cntIndent72" type="disc">
                      <li>Under <b class="ui">Settings</b>, click <b class="ui">Workflow settings</b>.</li>

                    </ul>
                    <ol class="cntIndent36" start="1" type="1">
                      <li>For a site content type:</li>
                    </ol>
                    <ul class="cntIndent72" type="disc">
                      <li>On the home page for the site collection, on the <b class="ui">Site Actions</b> menu <img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/140/014/ZA010074910.gif" alt="Menu image" title="Menu image" border="0">, point to <b class="ui">Site Settings</b>, and then click <b class="ui">Modify All Site Settings</b>.</li>

                      <li>Under <b class="ui">Galleries</b>, click <b class="ui">Site content types</b>.</li>
                      <li>Click the name of the site content type for which you want to add or change a workflow, and then click <b class="ui">Workflow settings</b>.</li>
                    </ul>
                    <p><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;If workflows have already been added to this list, library, or content type, this step takes you directly to the Change Workflow Settings page, and you need to click <b class="ui">Add a workflow</b> to go to the Add a Workflow page. If no workflows have been added to this list, library, or content type, this step takes you directly to the Add a Workflow page.</p>

                    <ol class="cntIndent36" start="1" type="1">
                      <li>On the Change Workflow Settings page, click <b class="ui">Add a workflow</b> or click the name of the workflow for which you want to change the settings.</li>
                      <li>Do one of the following: </li>
                      <ul type="disc">
                        <li>If you are adding a workflow, on the Add a Workflow page, in the <b class="ui">Workflow</b> section, click the <b class="ui">Collect Feedback</b> workflow template.</li>

                        <li>If you are changing the settings for a workflow, on the Change a Workflow page, change the settings that you want to change according to the following steps.</li>
                      </ul>
                      <li>In the <b class="ui">Name</b> section, type a unique name for the workflow.</li>
                    </ol>
                    <p>In the <b class="ui">Task List</b> section, specify a tasks list to use with this workflow.</p>

                    <p><b class="cntnote">&nbsp;Notes&nbsp;</b></p>
                    <ul class="cntIndent36" type="disc">
                      <li>You can use the default <b class="ui">Tasks</b> list or you can create a new one. If you use the default <b class="ui">Tasks</b> list, workflow participants will be able to find and view their workflow tasks easily by using the <b class="ui">My Tasks</b> view of the <b class="ui">Tasks</b> list.</li>

                      <li>If the tasks for this workflow will reveal sensitive or confidential data that you want to keep separate from the general <b class="ui">Tasks</b> list, you should create a new tasks list.</li>
                      <li>If your organization will have numerous workflows or if workflows will involve numerous tasks, you should create a new tasks list. In this instance, you might want to create tasks lists for each workflow.</li>
                    </ul>
                    <ol class="cntIndent36" start="4" type="1">
                      <li>In the <b class="ui">History List</b> section, select a history list to use with this workflow. The history list displays all of the events that occur during each instance of the workflow.</li>

                    </ol>
                    <p class="cntIndent36"><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;You can use the default <b class="ui">History</b> list or you can create a new one. If your organization will have numerous workflows, you might want to create a separate history list for each workflow.</p>
                    <ol class="cntIndent36" start="5" type="1">
                      <li>In the <b class="ui">Start Options</b> section, specify how, when, or by whom a workflow can be started. </li>
                    </ol>
                    <p class="cntIndent36"><b class="cntnote">&nbsp;Notes&nbsp;</b></p>

                    <ul class="cntIndent72" type="disc">
                      <li>Specific options may not be available if they are not supported by the workflow template that you selected.</li>
                      <li>The option <b class="ui">Start this workflow to approve publishing a major version of an item</b> is available only if support for major and minor versioning is enabled for the library and if the workflow template that you selected can be used for content approval.</li>
                    </ul>
                    <ol class="cntIndent36" start="6" type="1">
                      <li>If you are adding this workflow to a site content type, specify whether you want to add this workflow to all content types that inherit from this content type in the <b class="ui">Update List and Site Content Types</b> section.</li>

                    </ol>
                    <p class="cntIndent36"><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;The <b class="ui">Update List and Site Content Types</b> section appears on the Add a Workflow page only for site content types.</p>
                    <ol class="cntIndent36" start="7" type="1">
                      <li>Click <b class="ui">Next</b>.</li>
                      <li>On the Customize Workflow page, specify the options that you want for how tasks are routed, the default workflow start values, how the workflow is completed, and what actions happen when the workflow is successfully completed.</li>
                    </ol>

                    <p class="cntIndent36">Select options in any of the following sections. You are not required to specify options in every section:</p>
                    <p class="cntIndent36"><a class="DropDown" href="javascript:ToggleDiv('divExpCollAsst_207826400')"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/785/945/ZA079005000.gif" class="cntExpandoImg" alt="Show" title="Show" id="divExpCollAsst_207826400_img" border="0"><b class="ui">Workflow Tasks</b></a></p>
                    <div class="ACECollapsed" border="0" id="divExpCollAsst_207826400">
                      <div id="tableoverflow" class="cntIndent36">
                        <table class="collapse">
                          <tbody><tr class="trbgeven">
                            <th><b class="bterm">To</b></th>
                            <th><b class="bterm">Do this</b></th>

                          </tr>
                          <tr class="trbgodd">
                            <td>Assign tasks to all participants at once (parallel workflow)</td>
                            <td>Select the <b class="ui">All participants simultaneously (parallel)</b> button.</td>
                          </tr>
                          <tr class="trbgeven">

                            <td>
                              <p>Assign tasks to one participant at a time (serial workflow)</p>
                              <p>If you make the workflow a serial workflow, one participant must complete a task before the next participant receives a task</p>
                            </td>
                            <td>Select the <b class="ui">One participant at a time (serial)</b> button.</td>
                          </tr>

                          <tr class="trbgodd">
                            <td>Allow workflow participants to reassign their tasks to other people</td>
                            <td>Select the <b class="ui">Reassign the task to another person</b> check box.</td>
                          </tr>
                          <tr class="trbgeven">
                            <td>Allow workflow participants to request a change to the document or item to be approved before completing a task</td>

                            <td>Select the <b class="ui">Request a change before completing the task</b> check box.</td>
                          </tr>
                        </tbody></table>
                      </div>
                    </div>
                    <p class="cntIndent36"><a class="DropDown" href="javascript:ToggleDiv('divExpCollAsst_480128603')"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/785/945/ZA079005000.gif" class="cntExpandoImg" alt="Show" title="Show" id="divExpCollAsst_480128603_img" border="0"><b class="ui">Default Workflow Start Values</b></a></p>
                    <div class="ACECollapsed" border="0" id="divExpCollAsst_480128603">
                      <div id="tableoverflow" class="cntIndent36">

                        <table class="collapse">
                          <tbody><tr class="trbgeven">
                            <th><b class="bterm">To</b></th>
                            <th><b class="bterm">Do this</b></th>
                          </tr>
                          <tr class="trbgodd">
                            <td>Specify a default list of participants for all instances of this workflow</td>

                            <td>
                              <p>Type the names of people who you want to participate when this workflow is started, or click <b class="ui">Reviewers</b> to select people and groups from the directory service.</p>
                              <p><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;If you set up this workflow as a serial workflow, add the names of the workflow participants in the order in which you want the tasks to be assigned.</p>
                            </td>
                          </tr>
                          <tr class="trbgeven">

                            <td>Assign a single tasks to groups</td>
                            <td>
                              <p>Select the <b class="ui">Assign a single task to each group entered (Don't expand groups)</b> check box.</p>
                              <p>Select this option if you plan to specify groups as workflow participants, and you want only one task to be assigned to the group instead of individual tasks for every group member.</p>
                            </td>
                          </tr>

                          <tr class="trbgodd">
                            <td>Allow people who start the workflow to change or add participants</td>
                            <td>
                              <p>Select the <b class="ui">Allow changes to the participant list when this workflow is started</b> check box.</p>
                              <p>This option is selected by default. If you want to prevent people who start the workflow from being able to change or add participants, clear this check box.</p>
                            </td>

                          </tr>
                          <tr class="trbgeven">
                            <td>Specify a default message that appears with each task</td>
                            <td>Type a message or instructions in the text box.</td>
                          </tr>
                          <tr class="trbgodd">
                            <td>Specify a due date for parallel workflows</td>

                            <td>Type or select a date under <b class="ui">Tasks are due by (parallel)</b>.</td>
                          </tr>
                          <tr class="trbgeven">
                            <td>Specify how long serial workflow participants have to complete workflow tasks</td>
                            <td>Under <b class="ui">Give each person the following amount of time to finish their task (serial)</b>, type a number, and then select either <b class="ui">Day(s)</b> or <b class="ui">Week(s)</b> as the increment of time.</td>

                          </tr>
                          <tr class="trbgodd">
                            <td>Specify a list of people who should receive alerts (not task assignments) when the workflow is started</td>
                            <td>Under <b class="ui">Notify Others</b>, type the names of the people you want to be notified, or click <b class="ui">CC</b> to select people and groups from the directory service.</td>
                          </tr>

                        </tbody></table>
                      </div>
                    </div>
                    <p class="cntIndent36"><a class="DropDown" href="javascript:ToggleDiv('divExpCollAsst_144665521')"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/785/945/ZA079005000.gif" class="cntExpandoImg" alt="Show" title="Show" id="divExpCollAsst_144665521_img" border="0"><b class="ui">Complete the Workflow</b></a></p>
                    <div class="ACECollapsed" border="0" id="divExpCollAsst_144665521">
                      <div id="tableoverflow" class="cntIndent36">
                        <table class="collapse">
                          <tbody><tr class="trbgeven">
                            <th><b class="bterm">To</b></th>

                            <th><b class="bterm">Do this</b></th>
                          </tr>
                          <tr class="trbgodd">
                            <td>Specify that a parallel workflow is complete when a specific number of participants complete their tasks</td>
                            <td>
                              <p>Select the <b class="ui">Following number of tasks are finished</b> check box, and then type a number.</p>

                              <p><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;This option is not available if your workflow is a serial workflow.</p>
                            </td>
                          </tr>
                          <tr class="trbgeven">
                            <td>Specify that a workflow is complete when the document or item is rejected</td>
                            <td>Select the <b class="ui">Document is rejected</b> check box.</td>

                          </tr>
                          <tr class="trbgodd">
                            <td>Specify that a workflow is complete when the document or item is changed</td>
                            <td>Select the <b class="ui">Document is changed</b> check box.</td>
                          </tr>
                        </tbody></table>

                      </div>
                    </div>
                    <p class="cntIndent36"><a class="DropDown" href="javascript:ToggleDiv('divExpCollAsst_37882317')"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/785/945/ZA079005000.gif" class="cntExpandoImg" alt="Show" title="Show" id="divExpCollAsst_37882317_img" border="0"><b class="ui">Post-completion Workflow Activities</b></a></p>
                    <div class="ACECollapsed" border="0" id="divExpCollAsst_37882317">
                      <div id="tableoverflow" class="cntIndent36">
                        <table class="collapse">
                          <tbody><tr class="trbgeven">
                            <th><b class="bterm">To</b></th>
                            <th><b class="bterm">Do this</b></th>

                          </tr>
                          <tr class="trbgodd">
                            <td>Update the approval status for a document or item after the workflow is complete</td>
                            <td>
                              <p>Select the <b class="ui">Update the approval status (use this workflow to control content approval)</b> check box.</p>
                              <p>Select this option if you want to this workflow to manage content approval and you also selected the <b class="ui">Start this workflow to approve publishing a major version of an item</b> check box on the Add a Workflow page.</p>

                            </td>
                          </tr>
                        </tbody></table>
                      </div>
                    </div>
                    <ol class="cntIndent36" start="9" type="1">
                      <li>Click <b class="ui">OK</b>.</li>
                    </ol>
                    <p><a href="#top"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/206/661/ZA010077668.gif" alt="Top of Page" title="Top of Page" border="0"></a> <a href="#top" class="cntTopOfPage">Top of Page</a></p><a id="BM3" name="BM3"></a><h2><a name="BM3" id="BM3"></a>Start a Collect Feedback workflow on a document or item</h2>

                    <p>You can manually start a Collect Feedback workflow on a document or item directly from the list or library where it is saved. The options available to you when you start the workflow may vary depending on how that workflow was customized when it was added to the list, library, or content type for the item. You must have at least the Edit Items permission to start a workflow. Some workflows may require that you also have the Manage Lists permission to start a workflow on an document or item.</p>
                    <p><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;If you want to ensure that workflow participants receive e-mail alerts and reminders about their workflow tasks after you start a workflow, check with your server administrator to verify that e-mail is enabled for your site.</p>
                    <ol class="cntIndent36" start="1" type="1">
                      <li>If the list or library is not already open, click its name on the Quick Launch.</li>
                    </ol>
                    <p class="cntIndent36">If the name of your list or library does not appear, click <b class="ui">View All Site Content</b>, and then click the name of your list or library.</p>
                    <ol class="cntIndent36" start="2" type="1">
                      <li>Point to the name of the document or item for which you want to start a workflow, click the arrow that appears, and then click <b class="ui">Workflows</b>.</li>

                      <li>Under <b class="ui">Start a New Workflow</b>, click the name of the Collect Feedback workflow that you want to start.</li>
                      <li>Type the names of the people you want to review the document or item on the <b class="ui">Reviewers</b> line, or click <b class="ui">Reviewers</b> to select people and groups from the directory service.</li>
                    </ol>
                    <p class="cntIndent36"><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;If your workflow is a serial workflow, type or select the names of the workflow participants in the order in which you want the tasks to be assigned.</p>

                    <ol class="cntIndent36" start="5" type="1">
                      <li>If you are including groups as workflow participants, select the <b class="ui">Assign a single task to each group entered (Do not expand groups)</b> check box if you want only one task notification to be assigned to the group instead of individual task notifications for every group member.</li>
                      <li>If you want to include a message or specific task instructions, type this information in the text box under <b class="ui">Type a message to include with your request</b>.</li>
                      <li>To specify when the task should be completed, under <b class="ui">Due Date</b>, do one of the following:</li>

                      <ul type="disc">
                        <li>For a serial workflow, type a number, and then select either <b class="ui">Day(s)</b> or <b class="ui">Week(s)</b> as the increment of time.</li>
                        <li>For a parallel workflow, type or select a date under <b class="ui">Tasks are due by</b>.</li>
                        <li>If you want other people to receive notifications (not task assignments) when the workflow is started, type their names on the <b class="ui">CC</b> line, or click <b class="ui">CC</b> to select people and groups from the directory service.</li>

                      </ul>
                      <li>Click <b class="ui">Start</b>.</li>
                    </ol>
                    <p><a href="#top"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/206/661/ZA010077668.gif" alt="Top of Page" title="Top of Page" border="0"></a> <a href="#top" class="cntTopOfPage">Top of Page</a></p><a id="BM4" name="BM4"></a><h2><a name="BM4" id="BM4"></a>Complete a Collect Feedback workflow task</h2>
                    <p>Participants in an Collect Feedback workflow can complete their workflow tasks from either the list or library where the item or document is located or from directly within certain programs that are part of the 2007 Office release. For information about how to complete a workflow task in a client program, see the Help for that program.</p>
                    <h3>Complete a Collect Feedback workflow task on the server</h3>
                    <ol class="cntIndent36" start="1" type="1">

                      <li>Go to the <b class="ui">Tasks</b> list for the site, and then select <b class="ui">My Tasks</b> on the <b class="ui">View</b> menu to locate your workflow task.</li>
                    </ol>
                    <p class="cntIndent36"><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;If the workflow does not use the default <b class="ui">Tasks</b> list, then your workflow task may not appear in the <b class="ui">Tasks</b> list. To locate your workflow task, open the list or library where the workflow item is saved. Point to the item that you want, click the arrow that appears, and then click <b class="ui">Workflows</b>. Under <b class="ui">Running Workflows</b>, click the name of the workflow in which you are a participant. On the Workflow Status page, under <b class="ui">Tasks</b>, locate your workflow task.</p>

                    <ol class="cntIndent36" start="2" type="1">
                      <li>Point to the name of the task that you want to complete, click the arrow that appears, and then click <b class="ui">Edit Item</b>.</li>
                      <li>Do one of the following:</li>
                      <ul type="disc">
                        <li>To read or view the contents of the document or item, click the link to the item that displays at the top of the task form.</li>
                      </ul>
                    </ol>

                    <p class="cntIndent72">If you add comments or make changes directly in the document, be sure to save your changes to the server.</p>
                    <ul class="cntIndent72" type="disc">
                      <li>To provide feedback comments to the workflow owner, type your feedback in the text box that is provided, and then click <b class="ui">Send Feedback</b>.</li>
                      <li>To reassign the review task to another person, click <b class="ui">Reassign task</b>, specify to whom you want to assign the task, and then click <b class="ui">Send</b>.</li>
                      <li>To request a change to the item, click <b class="ui">Request a change</b>, specify to whom you want to assign the change request, provide information about the change requested, and then click <b class="ui">Send</b>.</li>

                    </ul>
                    <p class="cntIndent72"><b class="cntnote">&nbsp;Note&nbsp;</b>&nbsp;&nbsp;Depending on how the workflow was customized when it was added to the list, library, or content type for this item, the options to reassign the task or request a change may not be available.</p>
                    <p><a href="#top"><img style="visibility: visible;" src="http://officeimg.vo.msecnd.net/en-us/files/206/661/ZA010077668.gif" alt="Top of Page" title="Top of Page" border="0"></a> <a href="#top" class="cntTopOfPage">Top of Page</a></p></div><div class="cdFeedbackContainer dvRefresh" id="feedbackDiv"><div class="cdFeedbackTitle">Did this article help you?</div><div class="cdFeedbackButtonGroup"><span class="cdFeedbackButton"><input style="display: none;" value="Yes" type="button"><a style="min-width: 46px;" class="cdBtn" href="javascript:void(0)"><div class="cdBtnL"></div><div class="cdBtnM">Yes</div><div class="cdBtnR"></div></a></span><span class="cdFeedbackButton"><input style="display: none;" value="No" type="button"><a style="min-width: 44px;" class="cdBtn" href="javascript:void(0)"><div class="cdBtnL"></div><div class="cdBtnM">No</div><div class="cdBtnR"></div></a></span><span class="cdFeedbackButton"><input style="display: none;" value="Not what I was looking for" type="button"><a style="min-width: 167px;" class="cdBtn" href="javascript:void(0)"><div class="cdBtnL"></div><div class="cdBtnM">Not what I was looking for</div><div class="cdBtnR"></div></a></span></div></div><div class="cdclr">&nbsp;</div></div><div class="cdclr">&nbsp;</div></div></div><div class="cdArticleRight"><div id="adControl1" class="cdAdContainer"><div class="cdAdTitle"><div>advertisement</div><div id="adControl1_DispAd"><iframe src="about:blank" name="dapIfM0" id="dapIfM0" width="300" frameborder="0" height="250" scrolling="no"></iframe></div></div></div><div class="cdSeeAlso"><h4>See Also</h4><ul><li><a href="http://office.microsoft.com/en-us/sharepoint-server-help/redir/HA010172007.aspx?CTT=3" name="{&quot;a&quot;:&quot;HA010172007&quot;,&quot;at&quot;:null,&quot;d&quot;:&quot;Workflows must be added to a list, library, or content type to make them available for use on documents or items. In this article   What types of workflows a...&quot;,&quot;p&quot;:&quot;Provided by Microsoft&quot;,&quot;t&quot;:&quot;Article&quot;,&quot;u&quot;:null,&quot;uh&quot;:null}">Add or change a workflow for a list, library, or content type</a></li><li><a href="http://office.microsoft.com/en-us/sharepoint-server-help/redir/HA010154424.aspx?CTT=3" name="{&quot;a&quot;:&quot;HA010154424&quot;,&quot;at&quot;:null,&quot;d&quot;:&quot;Workflows help people to collaborate on documents and to manage project tasks by implementing business processes on documents and items in a  Microsoft Offic...&quot;,&quot;p&quot;:&quot;Provided by Microsoft&quot;,&quot;t&quot;:&quot;Article&quot;,&quot;u&quot;:null,&quot;uh&quot;:null}">Introduction to workflows</a></li><li><a href="http://office.microsoft.com/en-us/sharepoint-server-help/redir/HA010154428.aspx?CTT=3" name="{&quot;a&quot;:&quot;HA010154428&quot;,&quot;at&quot;:null,&quot;d&quot;:&quot;The Collect Signatures workflow routes a Microsoft Office document that is saved to a list or library to a group of people to collect their digital signature...&quot;,&quot;p&quot;:&quot;Provided by Microsoft&quot;,&quot;t&quot;:&quot;Article&quot;,&quot;u&quot;:null,&quot;uh&quot;:null}">Use a Collect Signatures workflow</a></li></ul></div></div></div>
                    """

    soup = BeautifulSoup(doc)
    return soup

def getUrlSoup(url):
    '''
    Get Beautiful Soup from a URL
    '''
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def basicFeatures():
    '''
    Demo some BeautifulSoup features and structure
    '''

    soup = getBasicSoup()

    printValue( "soup.prettify()", "\n" + soup.prettify() )
    print

    # HTML tagname
    printValue( "soup.contents[0].name" , soup.contents[0].name )

    # Head tag name
    printValue( "soup.contents[0].name" , soup.contents[0].contents[0].name )

    # Head Parent Tag name i.e. html
    head = soup.contents[0].contents[0]
    printValue( "head.parent.name" , head.parent.name)

    # Tag following head
    # Full Title tag
    printValue( "head.next" , head.next)

    # Next sibling tag name of the head tag
    # Body tag name
    printValue( "head.nextSibling.name" , head.nextSibling.name)

    # Contents of the next sibling tag (body) first tag
    # First paragraph tag and its elements
    printValue( "head.nextSibling.contents[0]" , head.nextSibling.contents[0])

    # Contents of the next sibling tag (body) first tag's next sibling
    # Second paragraph tag and its elements
    printValue( "head.nextSibling.contents[0].nextSibling" , head.nextSibling.contents[0].nextSibling)


def searchSoup():
    '''
    Examples of searching the soup for certain tags,
      or tags with certain properties
    '''

    soup = getBasicSoup()

    # Get the Actual Title tag element
    print "Get the Actual Title tag element"
    titleTag = soup.html.head.title
    print "titleTag = soup.html.head.title"
    printValue( "titleTag" , titleTag )
    print

    # String of the contents of titleTag, 'Page Title'
    print "String of the contents of titleTag, 'Page Title'"
    printValue( "titleTag.string" , titleTag.string )
    print

    # Number of occurrences of the 'p' tag in the soup
    print "Number of occurrences of the 'p' tag in the soup"
    printValue( "len( soup('p') )" , len( soup('p') ) )
    print

    # Find all of tags 'p' with the attribute ' align="center" '
    print "Find all of tags 'p' with the attribute 'align=\"center\"'"
    printValue( "soup.findAll('p', align=\"center\")" , soup.findAll('p', align="center") )
    print

    # Find the first child tag 'p' with the attribute ' align="center" '
    print "Find the first child tag 'p' with the attribute 'align=\"center\"'"
    printValue( "soup.find('p', align=\"center\")" , soup.find('p', align="center") )
    print

    # Find all tags 'p' with the attribute ' align="center" ' and get the value of 'id' for the first element
    print "Find the first child tag 'p' with the attribute 'align=\"center\"'"
    print "    and get the value of 'id' for the first element"
    printValue( "soup('p', align=\"center\")[0]['id']" , soup('p', align="center")[0]['id'] )
    print

    # Find the first child tag 'p' with the attribute where the align attribute matches the
    #   regular expression '^b.*', i.e. the attribute must start with the letter 'b', and get the value of the 'id'
    print "Find the first child tag 'p' with the attribute where the align attribute matches the"
    print "    regular expression '^b.*', i.e. the attribute must start with the letter 'b', and get the value of the 'id'"
    printValue( "soup.find('p', align=re.compile('^b.*') )['id']" , soup.find('p', align=re.compile('^b.*') )['id'] )
    print

    print "String of the contents of the 'b' of the first child tag 'p' ; 'one'"
    printValue( "soup.find('p').b.string" , soup.find('p').b.string )
    print

    print "String of the contents of the 'b' of the second child 'p' tag ; 'two'"
    printValue( "soup('p')[1].b.string" , soup('p')[1].b.string )
    print


def modifySoup():
    '''
    Examples of how easily soup can be modified
    '''

    soup = getBasicSoup()

    # Get the Actual Title tag element
    print "Get the Actual Title tag element"
    titleTag = soup.html.head.title
    print "titleTag = soup.html.head.title"
    printValue( "Original titleTag" , titleTag )

    # Add an 'id' attribute
    titleTag['id'] = 'theTitle'
    print "titleTag['id'] = 'theTitle'"
    printValue( "Updated with attribute titleTag" , titleTag )

    # Update the contents of the title tag
    titleTag.contents[0].replaceWith( "New title" )
    print "titleTag.contents[0].replaceWith( \"New title\" )"
    printValue( "New titleTag" , titleTag )
    print

    # Destructively rips the first child element 'p' out of the tree.
    print "Destructively rips the first child element 'p' out of the tree."
    soup.p.extract()
    print "soup.p.extract()"
    print soup.prettify()
    print

    # Replace the first child element 'p' with the first occurrance of the child element 'b'.
    #   Even if 'b' is a child of 'p'
    print "Replace the first child element 'p' with the first occurrance of the child element 'b'."
    print "Even if 'b' is a child of 'p'"
    soup.p.replaceWith(soup.b)
    print "soup.p.replaceWith(soup.b)"
    print soup.prettify()
    print

    # Insert a new child element at position 0 of the body tag, i.e. before the 'b' tag
    print "Insert a new child element at position 0 of the body tag, i.e. before the 'b' tag"
    soup.body.insert( 0 , "This page used to have " )
    print "soup.body.insert( 0 , \"This page used to have \" )"
    print
    # Insert a new child element at position 2 of the body tag, i.e. after the 'b' tag
    print "Insert a new child element at position 2 of the body tag, i.e. after the 'b' tag"
    soup.body.insert( 2 , " &lt;p&gt; tags! " )
    print "soup.body.insert( 2 , \"This page used to have \" )"
    printValue( "soup.body", soup.body )

def parseICCCommercialCrimeServicesWeeklyPiracyReport():
    '''
    Real World Example that fetches the ICC Commercial Crime Services weekly piracy report,
      Parses it with Beautiful Soup, and pulls out the piracy incidents
    '''

    page = None
    try:
        page = urllib2.urlopen( "http://www.icc-ccs.org/prc/piracyreport.php" )
    except urllib2.HTTPError, httpError:
        print "%(error)s; %(url)s" % { "error" : httpError , "url" : httpError.geturl() }
        page = None

    if page is not None:
        soup = BeautifulSoup( page )
        for incident in soup( 'td',  width="90%" ):
            where, linebreak, what = incident.contents[:3]
            print where.strip()
            print what.strip()
            print

def findAllInSoup():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'
        The most import of which are the name and keyword arguments.
    '''

    print "findAll with Name"
    findAllInSoupWithName()
    print "findAll with Keywords"
    findAllInSoupWithKeywords()
    print "findAll with Attrs"
    findAllInSoupWithAttrs()
    print "findAll by Css Class"
    findAllInSoupByCssClass()
    print "findAll with Text"
    findAllInSoupWithText()
    print "findAll with Recursive"
    findAllInSoupWithRecursive()
    print "findAll with Limit"
    findAllInSoupWithLimit()

def findAllInSoupWithName():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'

        Focusing on the name argument.
    '''
    soup = getBasicSoup()

    # 1. Simplest usage is to just pass in a tag name.
    #       This code finds all the <B> Tags in the document
    print "\n".join( (
        "1. Simplest usage is to just pass in a tag name.",
        "      This code finds all the <B> Tags in the document"
        ) )
    print

    printValue( "soup.findAll('b')" , soup.findAll('b') ,
        valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 2. You can also pass in a regular expression.
    #       This code finds all the tags whose name start with 'b'
    print "\n".join( (
        "2. You can also pass in a regular expression.",
        "      This code finds all the tags whose name start with 'b'"
        ) )
    print

    tagsStartingWithB = soup.findAll( re.compile('^b') )
    print "tagsStartingWithB = soup.findAll( re.compile('^b') )"
    printValue( "[tag.name for tag in tagsStartingWithB]" ,
                [tag.name for tag in tagsStartingWithB] ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 3. You can pass in a list or dictionary.
    #       These two calls find all the <TITLE> and all the <P> tags.
    #       They work the same way, but the second call runs faster
    print "\n".join( (
        "3. You can pass in a list or dictionary.",
        "      These two calls find all the <TITLE> and all the <P> tags.",
        "      They work the same way, but the second call runs faster"
        ) )
    print

    print "As a list:"
    printValue( "soup.findAll( [ 'title', 'p' ] )" , soup.findAll( [ 'title', 'p' ] ) ,
        indentLevel = 1, indentChar = "  ",
        valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    print "As a dictionary:"
    printValue( "soup.findAll( { 'title' : True , 'p' : True } )" , soup.findAll( { 'title' : True , 'p' : True } ) ,
        indentLevel = 1, indentChar = "  ",
        valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 4. You can pass in the special value True, which matches tag with a name:
    #       that is, it matches every tag. It may not look useful, but True is very
    #     useful when restricting attribute values.
    print "\n".join( (
        "4. You can pass in the special value True, which matches tag with a name:",
        "      that is, it matches every tag. It may not look useful, but True is very",
        "   useful when restricting attribute values."
        ) )
    print

    allTags = soup.findAll(True)
    print "allTags = soup.findAll(True)"
    printValue( "[tag.name for tag in allTags]" ,
                [tag.name for tag in allTags] ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 5. You can pass in a callable object which takes a Tag object as its only argument,
    #       and returns a boolean. Every Tag object that findAll encounters will be passed
    #     into this object, and if the call returns True then the tag is considered to match.
    print "\n".join( (
        "5. You can pass in a callable object which takes a Tag object as its only argument,",
        "      and returns a boolean. Every Tag object that findAll encounters will be passed",
        "   into this object, and if the call returns True then the tag is considered to match."
        ) )
    print

    # This code finds the tags that have two, and only two, attributes
    print "This code finds the tags that have two, and only two, attributes:"
    print
    printValue( "soup.findAll(lambda tag: len(tag.attrs) == 2)" ,
                soup.findAll(lambda tag: len(tag.attrs) == 2),
                valueIndentLevel = 1, valueIndentChar = "\n  ")

    # This code finds the tags that have one-character names and no attributes
    print "This code finds the tags that have two, and only two, attributes:"
    print
    printValue( "soup.findAll(lambda tag: len(tag.name) == 1 and len(tag.attrs) == 0)" ,
                soup.findAll(lambda tag: len(tag.name) == 1 and len(tag.attrs) == 0),
                valueIndentLevel = 1, valueIndentChar = "\n  ")

def findAllInSoupWithKeywords():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'

        Focusing on the keywords arguments which impose restrictions on the attributes of a tag.
    '''

    soup = getBasicSoup()

    # 1. Simple example finds all the tags which have a value of "center"
    #     for their "align" attribute
    print "\n".join( (
        '1. Simple example finds all the tags which have a value of "center"',
        '      for their "align" attribute'
        ) )
    print
    printValue( 'soup.findAll(align="center")' ,
                soup.findAll(align="center") ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 2. Simple example finds all the tags which have an "id" attribute
    #     value ending in "para" using a regular expression
    print "\n".join( (
        '2. Simple example finds all the tags which have an "id" attribute',
        '      value ending in "para" using a regular expression'
        ) )
    print
    printValue( 'soup.findAll(id=re.compile("para$")' ,
                soup.findAll(id=re.compile("para$")) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 3. Simple example finds all the tags where their "align" attribute is
    #     a value in the list [ "center" , "blah" ]
    print "\n".join( (
        '3. Simple example finds all the tags where their "align" attribute is',
        '      a value in the list [ "center" , "blah" ]'
        ) )
    print
    printValue( 'soup.findAll(align=[ "center" , "blah" ]' ,
                soup.findAll(align=[ "center" , "blah" ]) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 4. Simple example finds all the tags where their "align" attribute is
    #     value is not None and less than five characters
    print "\n".join( (
        '4. Simple example finds all the tags where their "align" attribute is',
        '      value is not None and less than five characters'
        ) )
    print
    printValue( 'soup.findAll(align=lambda(value): value and len(value) < 5)' ,
                soup.findAll(align=lambda(value): value and len(value) < 5) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 5. The special values True and None are of special interest.
    #     True matches a tag that has ANY value for the given attribute,
    #     and None matches a tag that has NO value for the given attribute.
    print "\n".join( (
        '5. The special values True and None are of special interest.',
        '      True matches a tag that has ANY value for the given attribute,',
        '      and None matches a tag that has NO value for the given attribute.'
        ) )
    print

    # Find all the tags with ANY value for the "align" attribute
    print 'Find all the tags with ANY value for the "align" attribute'
    printValue( 'soup.findAll(align=True)' ,
                soup.findAll(align=True) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # Find all the tags with NO value for the "align" attribute
    print 'Find all the tags names with NO value for the "align" attribute'
    printValue( '[ tag.name for tag in soup.findAll(align=None) ]' ,
                [ tag.name for tag in soup.findAll(align=None) ],
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print


def findAllInSoupWithAttrs():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'

        Focusing on the searching by attrs
    '''

    soup = getBasicSoup()

    # For the special case where the document has a tag that defines
    #   an attribute that is a keyword argument like "name" or a
    #   Python reserved word like "for". Beautiful Soup provides
    #   a special argument called attrs which is a dictionary that acts
    #   just like the keyword arguments
    print "\n".join( (
        'For the special case where the document has a tag that defines',
        '  an attribute that is a keyword argument like "name" or a',
        '  Python reserved word like "for". Beautiful Soup provides',
        '  a special argument called attrs which is a dictionary that acts',
        '  just like the keyword arguments'
        ) )
    print

    # Find all the tags with ending with "para" using a regular expression
    #   using the keyword arguments
    print 'Find all the tags with ending with "para" using a regular expression'
    print '  using the keyword arguments'
    keywordFindAll = soup.findAll( id = re.compile("para$") )
    printValue( 'soup.findAll( id = re.compile("para$") )' ,
                keywordFindAll,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # Find all the tags with ending with "para" using a regular expression
    #   using the attrs argument
    print 'Find all the tags with ending with "para" using a regular expression'
    print '  using the attrs argument'
    attrsFindAll = soup.findAll( attrs = { "id" : re.compile("para$") } )
    printValue( 'soup.findAll( attrs = { "id" : re.compile("para$") } )' ,
                attrsFindAll ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    print "Assert keyword-based findAll equals attrs-based argument findAll: %s" % ( keywordFindAll == attrsFindAll )
    assert keywordFindAll == attrsFindAll

def findAllInSoupByCssClass():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'

        Focusing on the searching by CSS class
    '''

    cssSoup = BeautifulSoup("""Bob's <b>Bold</b> Barbeque Saue now available
                            in <b class="hickory">Hickory</b> and
                            <b class="lime">Lime</a> for a limited time.""")
    print "cssSoup"
    print cssSoup.prettify()
    print

    # Searching by CSS class.
    #   The attrs argument can also be passed a string instead of a
    #   dictionary to restrict the CSS class.
    print "\n".join( (
        'Searching by CSS class.',
        '  The attrs argument can also be passed a string instead of a',
        '  dictionary to restrict the CSS class. '
        ) )
    print

    # Search for the CSS class attribute using a dictionary
    print "Search for the CSS class attribute using a dictionary"
    printValue( 'cssSoup.find( "b" , { "class" : "lime" } )' ,
                cssSoup.find( "b" , { "class" : "lime" } ) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # Search for the CSS class by passing a string to attribs
    print "Search for the CSS class by passing a string to attribs"
    printValue( 'cssSoup.find( "b", "hickory")' ,
                cssSoup.find( "b", "hickory") ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

def findAllInSoupWithText():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'

        Focusing on the searching with the text argument.

        "text" lets you search for NavigableString objects instead of Tags.
        Its value can be:
            - string
            - regular expression
            - list or dictionary
            - True or None
            - callable that takes a NavigableString as its argument
        ** If you use "text", then any values you give for "name" and **
        ** the keyword arguments are ignored.                   **
    '''

    soup = getBasicSoup()


    # 1. Get all of the NavigableString objects matching a simple string
    print '1. Get all of the NavigableString objects matching a simple string'
    print

    printValue( 'soup.findAll(text="one")' ,
                soup.findAll(text="one") ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 2. Get all of the NavigableString objects matching a unicode string
    print '2. Get all of the NavigableString objects matching a unicode string'
    print

    printValue("soup.findAll(text=u'one')" ,
                soup.findAll(text="one") ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 3. Get all of the NavigableString matches using a regular expression
    print '3. Get all of the NavigableString matches using a regular expression'
    print

    printValue('soup.findAll( text=re.compile("paragraph") ) ' ,
                soup.findAll( text=re.compile("paragraph") ) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 4. Get all of the NavigableString that have a value
    print '4. Get all of the NavigableString that have a value'
    print

    printValue('soup.findAll( text=True ) ' ,
                soup.findAll( text=True ) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 5. Get all of the NavigableString that are less
    #     than twelve characters in length.
    print '5. Get all of the NavigableString that are less'
    print '    than twelve characters in length.'
    print

    printValue('soup.findAll( text=lambda(x): len(x) < 12 ) ' ,
                soup.findAll( text=lambda(x): len(x) < 12 ) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

def findAllInSoupWithRecursive():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'

        Focusing on the searching with the recursive argument

        "recursive" is a boolean argument that defaults to True that acts as flag
          to tell Beautiful Soup whether to go all the way down the parse tree
          or only look at the immediate children of the Tag or parser object.
    '''

    soup = getBasicSoup()


    # 1. Get all of the names of all of the children Tag objects
    print '1. Get all of the names of all of the children Tag objects'
    print

    printValue( '[tag.name for tag in soup.html.findAll()]' ,
                        [tag.name for tag in soup.html.findAll()] ,
                        valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 2. Get all of the names of all of the children Tag objects with recursive=False
    print '2. Get all of the names of all of the children Tag objects with recursive=False'
    print

    printValue( '[tag.name for tag in soup.html.findAll(recursive=False)]' ,
                        [tag.name for tag in soup.html.findAll(recursive=False)] ,
                        valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

def findAllInSoupWithLimit():
    '''
    More in depth examples of searching the Parse Tree
        using the basic find method:
            'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'

        Focusing on the searching with the limit argument

        "limit" lets you stop the search once a certain number of matches are found.
    '''

    soup = getBasicSoup()


    # 1. Limit the search for "p" tags to "1"
    print '1. Limit the search for "p" tags to "1"'
    print

    printValue( 'soup.findAll( "p", limit=1 )' ,
                        soup.findAll( "p", limit=1 ) ,
                        valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

    # 2. Limit the search for "p" tags to "100"
    print '2. Limit the search for "p" tags to "100"'
    print

    printValue( 'soup.findAll( "p", limit=100 )' ,
                        soup.findAll( "p", limit=100 ) ,
                        valueIndentLevel = 1, valueIndentChar = "\n  ")
    print

def quickStart():
    '''
    Demonstrate some of the various features of BeautifulSoup
    '''

    # Demo some BeautifulSoup features and structure
    print
    print "Demo some BeautifulSoup features and structure"
    print "Calling basicFeatures()"
    print
    basicFeatures()

    # Examples of searching the soup for certain tags
    #   or tags with certain attributes
    print
    print " or ".join( ("Examples of searching the soup for certain tags" ,
                    "tags with certain attributes") )
    print "Calling searchSoup()"
    print
    searchSoup()

    # Examples of how easily soup can be modified
    print
    print "Examples of how easily soup can be modified"
    print "Calling modifySoup()"
    print
    modifySoup()

    # Real World Example that fetches the ICC Commercial Crime Services weekly piracy report,
    #   Parses it with Beautiful Soup, and pulls out the piracy incidents
    print
    print "Real World Example that fetches the ICC Commercial Crime Services weekly piracy report,"
    print "  Parses it with Beautiful Soup, and pulls out the piracy incidents"
    print "Calling parseICCCommercialCrimeServicesWeeklyPiracyReport()"
    print
    parseICCCommercialCrimeServicesWeeklyPiracyReport()


    # More in depth examples of searching the Parse Tree
    #   using the basic find method:
    #       'findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)'
    #   The most import of which are the name and keyword arguments.
    print
    print "More in depth examples of searching the Parse Tree"
    print "  using the basic find method:"
    print "      findAll(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)"
    print "  The most import of which are the name and keyword arguments."
    print "Calling findAllSoup()"
    print
    findAllInSoup()



if __name__ == "__main__":
    #quickStart()
    manipulateSoup()
    print "Get the Mega soup"
    outputSoup( getMegaSoup(), "megasoup.htm", 
        lambda (soup) : extractAllTags(soup, "div", "cdAdContainer") )
    printValue("Mega Soup", os.path.exists( "megasoup.htm" ) )

    print "Get the Big soup"
    outputSoup( getBigSoup(), "bigsoup.htm",
        lambda (soup) :
            extractAllTags(soup, "div",
                { "id" : lambda(idValue): idValue in ["cdnavcontbck"] }) )
    printValue("Big Soup", os.path.exists( "bigsoup.htm" ) )

    url = "http://office.microsoft.com/en-us/sharepoint-server-help/use-a-collect-feedback-workflow-HA010154426.aspx?CTT=3"
    print "Find First Ten Text"
    urlSoup = getUrlSoup(url)
    printValue( 'urlSoup.findAll(text=re.compile("^DOCTYPE html*"), limit = 10)' ,
                urlSoup.findAll(text=re.compile("^DOCTYPE html*"), limit = 10) ,
                valueIndentLevel = 1, valueIndentChar = "\n  ")
    
    print "Get the URL soup"
    outputSoup( getUrlSoup(url),
        "urlsoup.htm",
        lambda (soup) :
            extractAllTags(soup, "div",
                { "class" : lambda(cssClass): cssClass in ["cdAdContainer"] } ) ,
        lambda (soup) :
            extractAllTags(soup, "div",
                { "id" : lambda(idValue): idValue in ["cdnavcontbck"] } )
        ) 
    printValue("URL Soup", os.path.exists( "urlsoup.htm" ) )

    print "Get URL Soup PDF"
    outputSoupPDF(
        getUrlSoup(url),
        "urlsoup.pdf",
        "urlsoupPDF.htm",
        lambda (soup) :
            extractAllTags(soup, "div",
                { "class" : lambda(cssClass): cssClass in ["cdAdContainer"] } ) ,
        lambda (soup) :
            extractAllTags(soup, "div",
                { "id" : lambda(idValue): idValue in ["cdnavcontbck"] } )
        )

    print "complete"
    
    
