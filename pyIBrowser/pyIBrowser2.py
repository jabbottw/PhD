"""
/***************************************************************************
Name                 : pyIBrowser1
Description          : Tool set designed to download data over the internet
Date                 : 5/9/2014
copyright            : (C) 2014 by Julian Abbott-Whitley - PhD WFS
email                : jwhitley@phdwellfile.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program has been developed for use by PhD well file services.     *
 *                                                                         *
 ***************************************************************************/
 """
# Import necessary libraries
import mechanize
import requests
import sys
import os
import re
from bs4 import BeautifulSoup

# PostGreSQL data processor class
# Establishes a connection to a specified PG database so information can be queried as needed
class Phd_Browser:
        # Class initiation
        def __init__(self, word):
            print 'pyIBrowser initiated'
            
        # Allows for a file to be downloaded without using the object variables
        def Download_COGCC_Data(self, seqNum, fClass, outputDir):
            dlFile = False
            ##################################################################################################### Delete line below
            print "%s%s%s" % ("\nAPI: ", seqNum, "\n")
            # List variable to count the number of pages on the current COGCC web page
            pageLinks = ['1']
            # Counter - Some of the COGCC files have the same name. This variable allows us to create an 'index' number for every file
            fileCount = 1
            
            # Download COGCC files
            try:
                # Create a mechanize browser
                br = mechanize.Browser()
                # Include some headers that are recognized by the Microsoft server software
                br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
                # Get Site response
                response = br.open("%s%s" % ("http://ogccweblink.state.co.us/results.aspx?id=", seqNum))
                # Read site page html
                html = response.read()
                # Send html data to BeautifulSoup for collection
                soup = BeautifulSoup(html)
                
                # Cycle through the anchor elements. Identify javascript links so we can count the number of pages that we need to cycl through
                for a1 in soup.find_all('a'):
                    if "javascript:__doPostBack('WQResultGridView','Page$" in (a1.get('href')):
                        # Append java script text to the pageLinks list
                        pageLinks.append(a1.get_text())
                
                # Cycle through the index numbers starting from 0 up to the number of pages
                for ix in range(1, (len(pageLinks)+1)):
                    ##################################################################################################### Delete line below
                    print "%s%s%s" % ("\nPage: ", ix, "\n")
                    # Collect all anchor elements
                    anchors = soup.find_all('a')
                    # cycle from 1 up to the number of anchor elements
                    for jx in range(0, len(anchors)):
                        # Determine if the current anchor is a javascript header link
                        if "javascript:__doPostBack" in (anchors[jx].get("href")):
                            # Determine if the current anchor is a javascript page link
                            if "javascript:__doPostBack('WQResultGridView','Page$" in (anchors[jx].get("href")):
                                # Determine if the current anchor is a javascript page link that we want to click on
                                if "javascript:__doPostBack('WQResultGridView','Page$%s" % (ix + 1) in (anchors[jx].get("href")):
                                    # Select the javascript form
                                    br.select_form(nr=0)
                                    # Set the form to modifiable
                                    br.set_all_readonly(False)
                                    # Pass over necessary arguments to the javascript: __doPostBack function
                                    br["__EVENTTARGET"] = 'WQResultGridView'
                                    br["__EVENTARGUMENT"] = 'Page$%s' % (ix + 1)
                                    # update the response variable with the site response from br.submit
                                    response = br.submit()
                                    # Update html data
                                    html = response.read()
                                    # updates the soup objects
                                    soup = BeautifulSoup(html)
                                    
                                    ############################################################# Delete Line
                                    ##print "%s%s" % ("\n\nPAGE: ", ix + 1)

                                    
                            else:
                                pass
                        # We need to document the current class value of the current well. This well tell us if we should download the well based on the provided perameters
                        elif (jx-1) % 5 == 0:
                                dlFile = False
                                if fClass == "all":
                                    dlFile = True
                                elif fClass == "whfs" and (anchors[jx].get_text() == "Wells" or anchors[jx].get_text() == "Facilities" or anchors[jx].get_text() == "Operator"):
                                    dlFile = True
                                elif fClass == "logs" and anchors[jx].get_text() == "Well Logs" or anchors[jx].get_text() == "Projects":
                                    dlFile = True
                                else:
                                    dlFile = False
                        
                        # We want to download from every 4th link. The 4th link contains the name of the file. So download the file if the current (index-3) % 5 == 0
                        elif (jx-3) % 5 == 0 and dlFile == True:
                                # set the file name
                                fileName = "05" + seqNum + "0000_" + str(fileCount) + "_" + anchors[jx].get_text()
                                # Increment file count
                                fileCount = fileCount + 1
                                # Remove shity characters
                                fileName = re.sub('[\\\/:*?\'\"<>\|]','',fileName)
                                # Set the file path
                                filePath = os.path.join(outputDir, fileName)
                                # Set the url using the current anchor element href
                                url = "%s" % ("http://ogccweblink.state.co.us/" + anchors[jx].get("href"))
                                # Get it!!!!
                                
                                ##################################################################################################### Delete line below
                                print anchors[jx].get_text()
                                
                                r = requests.get(url)
                                if r.status_code == 200:
                                    with open(filePath, "wb") as image:
                                        image.write(r.content)
                                        
                                
                                
                        else:
                            pass
                # Clear out all variables
                br = None
                Soup = None
                html = None
                response = None
                fileName = None
                filePath = None
                url = None
                r = None
                return True
           
            except requests.ConnectionError, e:
                print 'Error %s%s' % (e, 'Couldn\'t establish a connection to the proovided url. Please check settings and try again.') 
                # Clear out all variables
                br = None
                Soup = None
                html = None
                response = None
                fileName = None
                filePath = None
                url = None
                r = None
                return False
                sys.exit(1)
        
        def Download_Utah_Data(self, seqNum, outputDir):
            # Download data
            try:
                # Set the file name
                fileName = "%s%s" % (seqNum, ".pdf")
                # Set the file path
                filePath = os.path.join(outputDir, fileName)
                # Set the url for the current download
                url = "%s%s%s%s" % ("http://oilgas.ogm.utah.gov/wellfiles/", seqNum[2:5],"/", fileName)
                # Get it!!!
                r = requests.get(url)
                if r.status_code == 200:
                    with open(filePath, "wb") as image:
                        image.write(r.content)
                # Clear out all variables
                fileName = None
                filePath = None
                url = None
                r = None
                return True
            
            except requests.ConnectionError, e:
                print 'Error %s%s' % (e, 'Couldn\'t establish a connection to the proovided url. Please check settings and try again.') 
                # Clear out all variables
                fileName = None
                filePath = None
                url = None
                r = None
                return False
                sys.exit(1)
            
            
        
            