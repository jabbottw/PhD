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
from PyQt4 import QtCore, QtGui 
from Ui_COGCC_Download import Ui_COGCC_Download
# create the dialog for COGCC_Download
class COGCC_DownloadDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_COGCC_Download ()
    self.ui.setupUi(self)

  def setAPITextBrowser(self, output):
    self.ui.ApiListBox.setText(output)

  def clearAPITextBrowser(self):
    self.ui.ApiListBox.clear()

  def setDirectory(self, dirPath):
    self.ui.OutputDirectoryTextBox.setText(dirPath)

  def setDownloadStatusBrowser(self, wellID):
    self.ui.downloadStatusBrowser.setText(wellID)

  def clearDownloadStatusBrowser(self):
    self.ui.downloadStatusBrowser.clear()

  def setReportDialogBrowser(self, inputMessage):
    self.ui.ReportDialog.setText(inputMessage)

  def clearReportDialogBrowser(self):
    self.ui.ReportDialog.clear()
