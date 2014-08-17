"""
/***************************************************************************
Name			 	 : COGCC_DL
Description          : Download well data from the COGCC website
Date                 : 30/Apr/14 
copyright            : (C) 2014 by Julian Abbott-Whitley - PhD WFS
email                : jwhitley@phdwellfile.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys, os
# Import the PyQt and QGIS libraries
from PyQt4 import QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import qgis.utils
import site
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialogs
from COGCC_DownloadDialog import COGCC_DownloadDialog

# Imports custom modules and classes
site.addsitedir(r'C:\Users\Julian\workspace\Eclipse\phd\dev')
from pyIBrowser import *
from pgAccessTool import *

class COGCC_Download: 

    def __init__(self, iface):
            # Create a custom DataProcessor object to interact with the PhD Postgresql database
            self.__DB_Processor = pgAccessTool.DB_Processor("phd", "postgres", "admin", "localhost", "5432")
            # Create a PyIBrowser Object for well data collection
            self.__iBrowser = pyIBrowser2.Phd_Browser("test")
            # Create an empty list to store all of the id values for the selected features in layer l
            self.__apiList = []
            # Attribute to note the state location of each well
            self._currentState = ""
            # Create a variable to store the directory
            self.__folder = ""
            # Create a variable to note which files to download for the COGCC data
            self.__COGCC_fClass = "all"
            # Create a variable to note if the current process is a PhD update, or a static download
            self.__phd_Update = False
            # variable to store a growing output message to the user
            self.__outputMessage = "Report Summary: \n"
            # Save reference to the QGIS interface
            self.iface = iface
            # Set a reference to our map canvas
            self.canvas = self.iface.mapCanvas()
            # Make a connection to the dialog 
            self.dlg = COGCC_DownloadDialog()
    
    #########################   Init GUI  #########################
    
    def initGui(self):  
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/COGCC_Download/icon.png"), "COGCC_DL", self.iface.mainWindow())
        # Create a connection for our API folder check box.
        # Allows the user to store data in one folder or several cataloged API folders. 
        QObject.connect(self.dlg.ui.SubDirCheckBox,SIGNAL("stateChanged(int)"),self.phdUpdateSelectionBox)
        # Create a connection to the "item download" list box
        QObject.connect(self.dlg.ui.listWidget,SIGNAL("currentRowChanged(int)"),self.updateDownloadSelection)
        # create a connection to setDirectoryButton button
        QObject.connect(self.dlg.ui.setDirectoryButton,SIGNAL("clicked()"),self.handleSetDirectoryButton)
        # create a connection to our updateWellListButton
        QObject.connect(self.dlg.ui.updateWellListButton,SIGNAL("clicked()"),self.handleUpdateWellListButton)
        # create a connection to our getSelectionToolButton
        QObject.connect(self.dlg.ui.getSelectionToolButton,SIGNAL("clicked()"),self.handleGetSelectionToolButton)
        # Create a connection to the get well data button
        QObject.connect(self.dlg.ui.getWellDataButton,SIGNAL("clicked()"),self.handlegetWellDataButton)
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.run)
        # Clear output messages
        self.dlg.clearReportDialogBrowser()
        self.dlg.clearDownloadStatusBrowser()
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&COGCC_DL", self.action)
    
    #########################   Event Handlers  #########################
    
    # Handles the set directory button
    def handleSetDirectoryButton(self):
        # Use the QtGui library to open a windows dialog selection window
        folder = QtGui.QFileDialog.getExistingDirectory(None, " ")
        # Need to format the directory to contain the necessary escape characters.
        # Split the folder directory on the \ character
        splitFolder = folder.split("\\")
        # tmp variable to help build the final path
        dirBuild = ""
        # Loop through each portion of the dir path and assemble the final path by inserting two \\    
        for i in splitFolder:
            dirBuild = "%s%s%s" % (dirBuild, i, "\\\\")
        # Create final directory path
        self.__folder = dirBuild
        # Pass the selected folder back to the UI.
        self.dlg.setDirectory( "%s" %(folder) )
    
    # Handles the update well list button 
    def handleUpdateWellListButton(self):
        # Clear the UI output messages
        self.dlg.clearReportDialogBrowser()
        self.dlg.clearDownloadStatusBrowser()
        # variable to store the currently selected layer
        l = self.canvas.currentLayer()
        # cycle through the selected features with layer l
        features = l.selectedFeatures()
        # Get the bounding state for the selected features
        self.__currentState = self.getBoundingState(features)
        # Update the well list based on the state reference
        if self.__currentState == "Colorado":
            # Update list using Colorado well data table
            self.updateCOWellList(features)
        elif self.__currentState == "Utah":
            # Update list using Utah well data table
            self.updateUTWellList(features)
        else:
            # Update list using default message
            self.updateEmptyWellList()
    
    # Handles the 'select wells' button trigger
    def handleGetSelectionToolButton(self):
        qgis.utils.iface.actionSelectRectangle().trigger()
    
    # Handles the COGCC download selection items   #############################################################################################################################
    def updateDownloadSelection(self, selection):
        if selection == 0:
            self.__COGCC_fClass = "all"
            self.createNewReportDialogMessage("%s" % ("All files selected for download"))
        elif selection == 1:
            self.__COGCC_fClass = "whfs"
            self.createNewReportDialogMessage("%s" % ("WHF's selected for download"))
        elif selection == 2:
            self.__COGCC_fClass = "logs"
            self.createNewReportDialogMessage("%s" % ("Logs selected for download"))
        else:
            self.__COGCC_fClass = ""
    
    # Updates the well status text box with the current well being processed  
    def updateWellStatusBox(self, current, total):
        dlsMessage = "Currently downloading data for well number %s of %s: " % (current, total)
        self.dlg.setDownloadStatusBrowser(dlsMessage)
        
    # Handles the check box state
    def phdUpdateSelectionBox(self,state):
        if (state==Qt.Checked):
            self.__phd_Update = True
            self.createNewReportDialogMessage("PhD update selected")
        else:
            self.__phd_Update = False
            self.createNewReportDialogMessage("Static download process selected")
    
    # Starts the data collection process##########################################################################################################
      
    def handlegetWellDataButton(self):
        # Clear the report dialog
        self.dlg.clearReportDialogBrowser()
        self.createNewReportDialogMessage("")
        if self.__phd_Update:
            print "Run phd update"
        # Cycle through the self.__apiList and pass each well id to the download module
        if len(self.__apiList) == 0:
            self.createErrorMessage("No Wells Selected.")
        else:
            for ix in range(len(self.__apiList)):
                # Send the index of the current well being processed to the UI 
                self.updateWellStatusBox((ix+1),len(self.__apiList))
                # Determine which state the well belongs to so we can utilize the necessary download method
                if self.__apiList[ix][0:2] == "05":
                    self.downloadCOGCC_Data(self.__apiList[ix])
                    dirLocMessage = "%s%s" % ("\nFiles downloaded to the following root directory: \n", self.__folder)
                elif self.__apiList[ix][0:2] == "43":
                    self.downloadUtah_Data(self.__apiList[ix])
                    dirLocMessage = "%s%s" % ("\nFiles downloaded to the following root directory: \n", self.__folder)
                else:
                    self.createErrorMessage("There has not been a process set up to pull data for the selected wells.")
            self.updateReportDialogMessage("%s" % (dirLocMessage))
          
    #########################   Utility Methods  #########################
    
    
    def getBoundingState(self, sFeatures):
        try:
            f = sFeatures[0]
            fGeom = f.geometry()
            fPointGeom = str(fGeom.asPoint())
            geomList = fPointGeom.split(",")
            latitude = geomList[0][1:len(geomList[0])]
            longitude = geomList[1][0:(len(geomList[1])-1)]
            stateList = self.__DB_Processor.getDBData("SELECT \"name\", geom FROM public.states WHERE ST_Contains(geom, ST_geomFromText('POINT(%s%s%s)', 4269))" % (latitude, " ", longitude))
            return stateList[0][0]
        except IndexError:
            self.createErrorMessage("Please make sure you have wells selected as well as the correct layer highlighted.")
    
    
    ###################### Update Well List Methods ##################      
    def updateCOWellList(self, coFeatures):
        # Clear the current API list
        self.__apiList = []
        # Arbitrary string to return selected api values to the UI
        apiOutputList = "API Numbers:\n"
        # output api variable to the API list text box
        for f in coFeatures:
            aIndex = f.fieldNameIndex('attrib_1')
            self.__apiList.append("%s" % (f.attributes()[aIndex]))
            apiOutputList = "%s%s%s" % (apiOutputList,f.attributes()[aIndex],"\n")
        # clear api list text box
        self.dlg.clearAPITextBrowser()
        # set api list text box
        self.dlg.setAPITextBrowser( "%s" %(apiOutputList) )
        # activate the qgis map interface selection tool
        qgis.utils.iface.actionSelectRectangle().trigger()
    
    
    def updateUTWellList(self, utFeatures):
        # Clear the current API list
        self.__apiList = []
        # Arbitrary string to return selected api values to the UI
        apiOutputList = "API Numbers:\n"
        # output api variable to the API list text box
        for f in utFeatures:
            aIndex = f.fieldNameIndex('API')
            self.__apiList.append("%s" % (str('{0:.10g}'.format(f.attributes()[aIndex]))))
            apiOutputList = "%s%s%s" % (apiOutputList,str('{0:.10g}'.format(f.attributes()[aIndex])),"\n")
        # clear api list text box
        self.dlg.clearAPITextBrowser()
        # set api list text box
        self.dlg.setAPITextBrowser( "%s" %(apiOutputList) )
        # activate the qgis map interface selection tool
        qgis.utils.iface.actionSelectRectangle().trigger()
    
    # Used in case the bounding state for the selected wells is not set correctly
    def updateEmptyWellList(self):
        # Clear the current API list
        self.__apiList = []
        # Arbitrary string to return selected api values to the UI
        apiOutputList = "API Numbers:\n No well selected"
        # clear api list text box
        self.dlg.clearAPITextBrowser()
        # set api list text box
        self.dlg.setAPITextBrowser( "%s" %(apiOutputList) )
        # activate the qgis map interface selection tool
        qgis.utils.iface.actionSelectRectangle().trigger()
    
    
    
    
    ###################### Update Report Dialog Methods ##################  #########################################################################################################
    
    def createNewReportDialogMessage(self, newMessage):
        # Clear the current report dialog browser                             
        self.dlg.clearReportDialogBrowser()
        # Update the output message                             
        self.__outputMessage = "%s%s" % ("Report Summary: \n", newMessage)
        # Update the ui report dialog                            
        self.dlg.setReportDialogBrowser( "%s" %(self.__outputMessage))
    
    def updateReportDialogMessage(self, message):
        # Update the output message with the input message
        self.__outputMessage = "%s%s%s" % (self.__outputMessage, "\n", message) 
        # Update the ui dialog report
        self.dlg.setReportDialogBrowser( "%s" %(self.__outputMessage))
    
    def createErrorMessage(self, eMessage):
        # Clear the current report dialog browser                             
        self.dlg.clearReportDialogBrowser()
        # Update the output message                             
        errorMessage = "%s%s" % ("Error Message: \n", eMessage)
        # Update the ui report dialog                            
        self.dlg.setReportDialogBrowser( "%s" %(errorMessage))
    
        
    
    ###################### Well Download Methods ##################
    # Start COGCC Download process  
    def downloadCOGCC_Data(self, currentAPI):
        # Clean the COGCC API string, returns a full API value
        cleanApi = self.__DB_Processor.cleanCO_API(currentAPI)
        # If the phd_Update variable is set to False, then this is a static download. Just download the files, without referencing the database. 
        if self.__phd_Update == False:
            dlStatus = self.__iBrowser.Download_COGCC_Data(cleanApi[2:10], self.__COGCC_fClass, self.__folder)
            self.updateReportDialogMessage("%s%s" % (currentAPI, " --- Files Downloaded"))
        # Otherwise, check the database to see if the current well has already been processed. If it hasn't, then process the current well. 
        else:
            # Check to see if the current well is stored in the database and is marked as processed
            sql = "select * from colorado.dl_report where dl_report.api = '%s' AND download = 'Completed'" % (cleanApi)
            dbList = self.__DB_Processor.getDBData(sql)
            if not dbList:
                '''If the current well is ####### NOT ####### found in the data base, then start the cycle to collect data for this well'''
                dlStatus = self.__iBrowser.Download_COGCC_Data(cleanApi[2:10], self.__COGCC_fClass, self.__folder)
                self.updateReportDialogMessage("%s%s" % (currentAPI, " --- Files Downloaded"))
            else:
                self.updateReportDialogMessage("%s%s" % (currentAPI, " --- already collected"))
    
    def downloadUtah_Data(self, currentAPI):
        # Start Utah download process
        # Query data base to see if data has been downloaded for the current well
        dbList = self.__DB_Processor.getDBData("select * from utah.ut_whf_dl_status where api_10 = '%s' AND well_proce = 'True'" %(currentAPI))
        # If the dbList is empty, then the current well is not marked as processed in the data base, try and download data for this well. 
        if not dbList:
            # Download data for the current well
            dlStatus = self.__iBrowser.Download_Utah_Data(currentAPI, self.__folder)
            # Update the current well within the database
            # Figure out if the current well exists in the DB
            wellExists = self.__DB_Processor.getDBData("select * from utah.ut_whf_dl_status where api_10 = '%s'" %(currentAPI))
            # If well exists, update the status with the boolean results of the download
            if wellExists:
                sqlInput = "UPDATE utah.ut_whf_dl_status SET well_proce = '%s' WHERE api_10 = '%s'" % (dlStatus,currentAPI)
                self.__DB_Processor.inputDBData(sqlInput)
                sqlInput = ""
            # Else add the well and update the status
            else:
                sqlInput = ("INSERT INTO utah.ut_whf_dl_status (gid, api_10, api_14, well_proce, api_county)"
                "VALUES ((select (max(gid)+1) from utah.ut_whf_dl_status),'%s','%s','%s','%s')" % (currentAPI, currentAPI + '0000', dlStatus, str(currentAPI[2:5])))
                self.__DB_Processor.inputDBData(sqlInput)
                sqlInput = ""
            self.updateReportDialogMessage("%s%s" % (currentAPI, " --- File Downloaded"))
        # Other wise, update the ui message to say that the current well has already been processed and move on to the next well.
        else:
            self.updateReportDialogMessage("%s%s" % (currentAPI, " --- already collected"))
    
    
    ######################### Unload & Run #########################
          
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&COGCC_DL",self.action)
        self.iface.removeToolBarIcon(self.action)
    
    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        result = self.dlg.exec_() 
        # See if OK was pressed
        if result == 1:
            self.dlg.clearReportDialogBrowser()
            self.dlg.clearAPITextBrowser()
            self.dlg.clearDownloadStatusBrowser()
        else:
            self.dlg.clearReportDialogBrowser()
            self.dlg.clearAPITextBrowser()
            self.dlg.clearDownloadStatusBrowser()
      
    
      
