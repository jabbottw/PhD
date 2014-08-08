# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_COGCC_Download.ui'
#
# Created: Thu May 29 14:16:40 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_COGCC_Download(object):
    def setupUi(self, COGCC_Download):
        COGCC_Download.setObjectName(_fromUtf8("COGCC_Download"))
        COGCC_Download.resize(502, 450)
        self.buttonBox = QtGui.QDialogButtonBox(COGCC_Download)
        self.buttonBox.setGeometry(QtCore.QRect(320, 250, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.ApiListBox = QtGui.QTextBrowser(COGCC_Download)
        self.ApiListBox.setGeometry(QtCore.QRect(10, 150, 101, 131))
        self.ApiListBox.setObjectName(_fromUtf8("ApiListBox"))
        self.SubDirCheckBox = QtGui.QCheckBox(COGCC_Download)
        self.SubDirCheckBox.setGeometry(QtCore.QRect(20, 80, 131, 31))
        self.SubDirCheckBox.setObjectName(_fromUtf8("SubDirCheckBox"))
        self.setDirectoryButton = QtGui.QToolButton(COGCC_Download)
        self.setDirectoryButton.setGeometry(QtCore.QRect(450, 40, 31, 21))
        self.setDirectoryButton.setObjectName(_fromUtf8("setDirectoryButton"))
        self.getSelectionToolButton = QtGui.QPushButton(COGCC_Download)
        self.getSelectionToolButton.setGeometry(QtCore.QRect(130, 150, 111, 23))
        self.getSelectionToolButton.setObjectName(_fromUtf8("getSelectionToolButton"))
        self.label = QtGui.QLabel(COGCC_Download)
        self.label.setGeometry(QtCore.QRect(10, 120, 111, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(COGCC_Download)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 121, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.OutputDirectoryTextBox = QtGui.QTextEdit(COGCC_Download)
        self.OutputDirectoryTextBox.setGeometry(QtCore.QRect(13, 40, 421, 31))
        self.OutputDirectoryTextBox.setObjectName(_fromUtf8("OutputDirectoryTextBox"))
        self.updateWellListButton = QtGui.QPushButton(COGCC_Download)
        self.updateWellListButton.setGeometry(QtCore.QRect(130, 180, 111, 23))
        self.updateWellListButton.setObjectName(_fromUtf8("updateWellListButton"))
        self.listWidget = QtGui.QListWidget(COGCC_Download)
        self.listWidget.setGeometry(QtCore.QRect(330, 120, 161, 71))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.downloadStatusBrowser = QtGui.QTextBrowser(COGCC_Download)
        self.downloadStatusBrowser.setGeometry(QtCore.QRect(130, 240, 191, 41))
        self.downloadStatusBrowser.setObjectName(_fromUtf8("downloadStatusBrowser"))
        self.StatusLabel = QtGui.QLabel(COGCC_Download)
        self.StatusLabel.setGeometry(QtCore.QRect(130, 210, 111, 21))
        self.StatusLabel.setObjectName(_fromUtf8("StatusLabel"))
        self.label_3 = QtGui.QLabel(COGCC_Download)
        self.label_3.setGeometry(QtCore.QRect(340, 80, 121, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.getWellDataButton = QtGui.QCommandLinkButton(COGCC_Download)
        self.getWellDataButton.setGeometry(QtCore.QRect(330, 200, 161, 41))
        self.getWellDataButton.setObjectName(_fromUtf8("getWellDataButton"))
        self.ReportDialog = QtGui.QTextBrowser(COGCC_Download)
        self.ReportDialog.setGeometry(QtCore.QRect(10, 330, 481, 111))
        self.ReportDialog.setObjectName(_fromUtf8("ReportDialog"))
        self.label_4 = QtGui.QLabel(COGCC_Download)
        self.label_4.setGeometry(QtCore.QRect(10, 300, 121, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(COGCC_Download)
        self.label_5.setGeometry(QtCore.QRect(340, 100, 121, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(COGCC_Download)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), COGCC_Download.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), COGCC_Download.reject)
        QtCore.QMetaObject.connectSlotsByName(COGCC_Download)

    def retranslateUi(self, COGCC_Download):
        COGCC_Download.setWindowTitle(_translate("COGCC_Download", "COGCC_Download", None))
        self.SubDirCheckBox.setText(_translate("COGCC_Download", "Update PhD Data", None))
        self.setDirectoryButton.setText(_translate("COGCC_Download", "...", None))
        self.getSelectionToolButton.setText(_translate("COGCC_Download", "Select Wells", None))
        self.label.setText(_translate("COGCC_Download", "API List", None))
        self.label_2.setText(_translate("COGCC_Download", "Output Directory", None))
        self.OutputDirectoryTextBox.setHtml(_translate("COGCC_Download", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Select output directory</span></p></body></html>", None))
        self.updateWellListButton.setText(_translate("COGCC_Download", "Update Well List", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("COGCC_Download", "Download all files", None))
        item = self.listWidget.item(1)
        item.setText(_translate("COGCC_Download", "Download WHFs only", None))
        item = self.listWidget.item(2)
        item.setText(_translate("COGCC_Download", "Download logs only", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.StatusLabel.setText(_translate("COGCC_Download", "Downlaod Status", None))
        self.label_3.setText(_translate("COGCC_Download", "Select files to download", None))
        self.getWellDataButton.setText(_translate("COGCC_Download", "Get Well Data", None))
        self.label_4.setText(_translate("COGCC_Download", "Report Dialog", None))
        self.label_5.setText(_translate("COGCC_Download", "(COGCC Only)", None))

