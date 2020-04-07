import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMainWindow, QAction, QHeaderView, QMenuBar
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox, QAction
import os
import read_ini_config
import datetime
import re as regEx
from datetime import datetime
import time
# global masterPath, blHubPath, master, blHub

# Create an application
app = QtWidgets.QApplication([])

# And a window5
win = QtWidgets.QWidget()
win.setWindowTitle('CTCOB17-BLMS On-Boarding Validation')
# win.setFixedSize(900, 600)
win.showMaximized()
base_path = os.getcwd()

# And give it a layout QGridLayout
layout = QtWidgets.QGridLayout()
win.setLayout(layout)

# add application icon
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("icons/atombondelectronmoleculescience_123078.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
win.setWindowIcon(icon)

# A components of widgets
selectComboBox = QtWidgets.QComboBox()
validateButton = QtWidgets.QPushButton('Start Validation')
browseMasterPath = QtWidgets.QPushButton('Browse Shared Template')
browseBlHubPath = QtWidgets.QPushButton('Browse Web Extracted Data')
masterPathText = QtWidgets.QLineEdit()
masterPathText.setReadOnly(True)
blHubPathText = QtWidgets.QLineEdit()
blHubPathText.setReadOnly(True)
logViewer = QtWidgets.QPlainTextEdit()

# Add the QWebViews to the layout
layout.addWidget(selectComboBox, 0, 1)
layout.addWidget(masterPathText, 1, 1)
layout.addWidget(blHubPathText, 2, 1)
layout.addWidget(browseMasterPath, 1, 2)
layout.addWidget(browseBlHubPath, 2, 2)
layout.addWidget(validateButton, 3, 2)
layout.addWidget(logViewer, 4, 0, 2, 3)
font = QtGui.QFont()
font.setPointSize(12)
logViewer.setFont(font)

# read config value for combobox list item
f = read_ini_config.read_config("Sections", "sections")
configItems = f.strip().split(',')
for item in configItems:
    selectComboBox.addItem(item)
tempPath = read_ini_config.read_config("Path", "TempPath")

# remove temp file
if os.path.exists(tempPath + "webExtractedRowsTemp"):
    os.remove(tempPath + "webExtractedRowsTemp")


def startValidation():
    global blRows, masterRenewalFrequencyPerCTAudit_Other
    global masterPath, blHubPath, master, blHub, statesColumn
    # readConfiguration()
    logViewer.clear()
    masterExcelFile = masterPathText.text()
    logViewer.appendPlainText("Reading master template data in excel...")
    QtGui.QGuiApplication.processEvents()
    time.sleep(1)
    blHubExcelFile = blHubPathText.text()
    logViewer.appendPlainText("Reading website extracted data in excel...")
    QtGui.QGuiApplication.processEvents()
    time.sleep(1)
    # master = master.strip().split(',')
    # masterExcelFile = pd.read_excel(masterExcelFile)
    # blHubExcelFile = pd.read_excel(blHubExcelFile)
    contentSet = selectComboBox.currentText()

    if contentSet == "Assumed Names":
        rowStart = 0
        columnStart = 0,1,3
        # print(masterPathText.text())
        masterBusinessColumns = pd.read_excel(masterPathText.text(), header=0, keep_default_na=False)
        blDataColumns = pd.read_excel(blHubPathText.text(), header=0, keep_default_na=False)
        masterBusinessdFrame = pd.DataFrame(masterBusinessColumns)
        blDataFrame = pd.DataFrame(blDataColumns)
        blDataFrame2 = pd.DataFrame(blDataColumns, columns=['License Name', 'License Authority'])

        masterBusinessdFrame = masterBusinessdFrame[['Owner/Registrant Name', 'DBA/Assumed/Fictitious Name', 'License Type']]
        blDataFrame = blDataFrame[['License Name']]

        masterBusinessdFrame['Owner/Registrant Name'] = masterBusinessdFrame['Owner/Registrant Name'].str.strip()
        masterBusinessdFrame['DBA/Assumed/Fictitious Name'] = masterBusinessdFrame['DBA/Assumed/Fictitious Name'].str.strip()
        masterBusinessdFrame['License Type'] = masterBusinessdFrame['License Type'].str.strip()
        # masterBusinessdFrame['License Authority'] = masterBusinessdFrame['License Authority'].str.strip()

        masterBusinessdFrame['masterBusiness1'] = masterBusinessdFrame['Owner/Registrant Name'].str.cat(
            masterBusinessdFrame['DBA/Assumed/Fictitious Name'], sep=" dba ")
        masterBusinessdFrame['masterBusinessdFrame'] = masterBusinessdFrame['masterBusiness1'].str.cat(
            masterBusinessdFrame['License Type'], sep=" - ")
        # masterBusinessdFrame['masterBusinessdFrame'] = masterBusinessdFrame['masterBusiness1'].str.cat(
            # masterBusinessdFrame['License Authority'], sep=" - ")

        masterBusinessdFrame['masterBusinessdFrame'] = masterBusinessdFrame['masterBusinessdFrame']
        blDataFrame['LicenseName'] = blDataFrame[['License Name']]
        # blDataFrame2['LicenseDuplicate'] = blDataFrame2[['License Name','License Authority']]
        for timer in reversed(range(1, 5)):
            logViewer.appendPlainText("Gathering data in " + str(timer) + " seconds...")
            QtGui.QGuiApplication.processEvents()
            time.sleep(1)
        for masterRows in masterBusinessdFrame.index:
            masterData = masterBusinessdFrame['masterBusinessdFrame'][masterRows]
            masterLAuthority = masterBusinessColumns.iloc[masterRows,4]
            masterLAuthority = regEx.sub(r'\n', ' ', str(masterLAuthority))
            masterLAuthority = regEx.sub(r'[;:,]', '', str(masterLAuthority))
            for blRows in blDataFrame.index:
                blData = blDataFrame['LicenseName'][blRows]
                blLAuthority = blDataColumns.iloc[blRows,11]
                blLAuthority = regEx.sub(r'\n', ' ', str(blLAuthority))
                blLAuthority = regEx.sub(r'[;:,]', '', str(blLAuthority))
                if masterData + "-" + masterLAuthority == blData + "-" + blLAuthority:
                    # start comparison here --master--
                    masterBusinessColumns.fillna('', inplace=True)
                    blDataColumns.fillna('', inplace=True)
                    masterLicenseNumber = masterBusinessColumns.iloc[masterRows,2]
                    masterLicenseNumber = regEx.sub(r'\n', ' ', str(masterLicenseNumber))
                    masterLicenseNumber = regEx.sub(r'[;:,]', '', str(masterLicenseNumber))
                    masterLicenseNumber = regEx.sub(r'# ', '#', str(masterLicenseNumber))
                    masterLicensingAuthority = masterBusinessColumns.iloc[masterRows,4].lower()
                    masterLicensingAuthority = regEx.sub(r'\n', ' ', str(masterLicensingAuthority))
                    masterLicensingAuthority = regEx.sub(r'[;:,]', '', str(masterLicensingAuthority))
                    masterStateProvince = masterBusinessColumns.iloc[masterRows,5].lower()
                    masterStatusPerCTAudit = masterBusinessColumns.iloc[masterRows,7].lower()
                    if masterStatusPerCTAudit == "no record" or masterStatusPerCTAudit == "cannot locate" or masterStatusPerCTAudit == "expired" or masterStatusPerCTAudit == "past due" or masterStatusPerCTAudit == "delinquent" or masterStatusPerCTAudit == "suspended":
                        masterStatusPerCTAudit = "inactive"  # PD feedback 12142019
                    masterRenewalDatePerCTAudit = masterBusinessColumns.iloc[masterRows,8]
                    if masterRenewalDatePerCTAudit == "N/A":
                        masterRenewalDatePerCTAudit = ""  # PD feedback 12142019
                    masterRenewalFrequencyPerCTAudit = masterBusinessColumns.iloc[masterRows,9]
                    if masterRenewalFrequencyPerCTAudit == "annual":
                        masterRenewalFrequencyPerCTAudit = "1 years"
                    if masterRenewalFrequencyPerCTAudit == "biennial":
                        masterRenewalFrequencyPerCTAudit = "2 years"
                    if masterRenewalFrequencyPerCTAudit == "triennial":
                        masterRenewalFrequencyPerCTAudit = "3 years"
                    #--BLHub--
                    blLicenseNumber = blDataColumns.iloc[blRows,2]
                    blLicenseNumber = regEx.sub(r'\n', ' ', str(blLicenseNumber))
                    blLicenseNumber = regEx.sub(r'[;:,]', '', str(blLicenseNumber))
                    blLicenseNumber = regEx.sub(r'# ', '#', str(blLicenseNumber))
                    blLicenseAuthority = blDataColumns.iloc[blRows,11].lower()
                    blLicenseAuthority = regEx.sub(r'\n', ' ', str(blLicenseAuthority))
                    blLicenseAuthority = regEx.sub(r'[;:,]', '', str(blLicenseAuthority))
                    blStateProvince = blDataColumns.iloc[blRows,13].lower()
                    blStatus = blDataColumns.iloc[blRows,7].lower()
                    blRenewalDueDate = blDataColumns.iloc[blRows,26]
                    blRenewalType = blDataColumns.iloc[blRows,24].lower()  # optional for frequency used only
                    if masterRenewalFrequencyPerCTAudit == "perpetual" or masterRenewalFrequencyPerCTAudit == "n/a":
                        if masterRenewalFrequencyPerCTAudit == blRenewalType:
                            masterRenewalFrequencyPerCTAudit_Other = "Match"
                        else:
                            masterRenewalFrequencyPerCTAudit_Other = "MisMatch"
                            logViewer.appendPlainText(str(masterData) + ": master Renewal Frequency Per CT Audit[" + str(masterRenewalFrequencyPerCTAudit) + "] not match with BL Hub Renewal Type[" + str(blRenewalType) + "]")
                            QtGui.QGuiApplication.processEvents()
                    blRecurrencePattern = blDataColumns.iloc[blRows,27].lower()
                    # --Compare List--
                    if str(masterLicenseNumber) != str(blLicenseNumber):
                        logViewer.appendPlainText(str(masterData) + ": master License Number[" + str(masterLicenseNumber) + "] not match with BL Hub License Number[" + str(blLicenseNumber) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterLicensingAuthority) != str(blLicenseAuthority):
                        logViewer.appendPlainText(str(masterData) + ": master Licensing Authority[" + str(masterLicensingAuthority) + "] not match with BL Hub License Authority[" + str(blLicenseAuthority) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterStateProvince) != str(blStateProvince):
                        logViewer.appendPlainText(str(masterData) + ": master State/Province[" + str(masterStateProvince) + "] not match with BL Hub State/Province[" + str(blStateProvince) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterStatusPerCTAudit) != str(blStatus):
                        logViewer.appendPlainText(str(masterData) + ": master Status Per CT Audit[" + str(masterStatusPerCTAudit) + "] not match with BL Hub Status[" + str(blStatus) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterRenewalDatePerCTAudit) != str(blRenewalDueDate):
                        logViewer.appendPlainText(str(masterData) + ": master Renewal Date Per CT Audit[" + str(masterRenewalDatePerCTAudit) + "] not match with BL Hub Renewal Due Date[" + str(blRenewalDueDate) + "]")
                        QtGui.QGuiApplication.processEvents()
                    #if str(masterRenewalFrequencyPerCTAudit) != str(blRenewalType):
                     #   logViewer.appendPlainText(str(masterData) + ": master Renewal Frequency Per CT Audit[" + str(masterRenewalFrequencyPerCTAudit) + "] not match with BlHub Renewal Type[" + str(blRenewalType) + "]")
                      #  QtGui.QGuiApplication.processEvents()
                    #if str(masterRenewalFrequencyPerCTAudit_Other) == "MisMatch":
                     #   logViewer.appendPlainText(str(masterData) + ": master Renewal Frequency Per CT Audit[" + str(masterRenewalFrequencyPerCTAudit) + "] not match with BlHub Renewal Type[" + str(blRenewalType) + "]")
                      #  QtGui.QGuiApplication.processEvents()
                    break
                # print(len(blDataFrame))
                if blRows == len(blDataFrame) - 1:
                    logViewer.appendPlainText(str(masterData) + ": not found in BlHubList!")
                    QtGui.QGuiApplication.processEvents()

        # search for duplicates
        duplicateRowsDF = blDataFrame2[blDataFrame2.duplicated(['License Name', 'License Authority'])]
        duplicateRowsDF = duplicateRowsDF.to_string()
        logViewer.appendPlainText("==============================================================")
        logViewer.appendPlainText("Found duplicate values: \n" + duplicateRowsDF)
        QtGui.QGuiApplication.processEvents()

        #check for missing 'dba' word
        missingDBA = blDataFrame['LicenseName'].str.contains(" dba ")
        for indexDba in missingDBA.index:
            misingDbaRow = missingDBA[indexDba]
            if misingDbaRow == False:
                missingDbaRowValue = blDataFrame['LicenseName'][indexDba]
                logViewer.appendPlainText("==============================================================")
                logViewer.appendPlainText("Rows with missing dba: \n" + missingDbaRowValue)
                QtGui.QGuiApplication.processEvents()
        # --compare count of rows
        logViewer.appendPlainText("==============================================================")
        QtGui.QGuiApplication.processEvents()
        BlHubRowCounts = blDataFrame.shape[0]
        masterRowCounts = masterBusinessdFrame.shape[0]
        if BlHubRowCounts != masterRowCounts:
            logViewer.appendPlainText("\nRow Matching of Master Against BlHub:\nMaster count of rows:[" + str(
                masterRowCounts) + "] is not match with [" + str(BlHubRowCounts) + "]!")
            QtGui.QGuiApplication.processEvents()

    if contentSet == "Business Licenses":
        rowStart = 0
        columnStart = 0,2
        masterBusinessColumns = pd.read_excel(masterPathText.text(), header=0, keep_default_na=False)
        blDataColumns = pd.read_excel(blHubPathText.text(), header=0, keep_default_na=False)
        masterBusinessdFrame = pd.DataFrame(masterBusinessColumns)
        blDataFrame = pd.DataFrame(blDataColumns)

        masterBusinessdFrame = masterBusinessdFrame[['Entity Name', 'License Type', 'License Number']]
        blDataFrame = blDataFrame[['License Name', 'License Number']]

        masterBusinessdFrame['License Number'] = masterBusinessdFrame['License Number'].astype(str)
        masterBusinessdFrame['masterBusiness1'] = masterBusinessdFrame['Entity Name'].str.cat(masterBusinessdFrame['License Type'], sep=" - ")
        masterBusinessdFrame['masterBusinessdFrame'] = masterBusinessdFrame['masterBusiness1'].str.cat(masterBusinessdFrame['License Number'], sep=" ")

        blDataFrame['License Number'] = blDataFrame['License Number'].astype(str)
        blDataFrame['License Number'] = blDataFrame['License Number'].str.strip(r'\r\n')
        blDataFrame['blDataBusiness'] = blDataFrame['License Name'].str.cat(blDataFrame['License Number'], sep=" ")
        for timer in reversed(range(1, 8)):
            logViewer.appendPlainText("Gathering data " + str(timer) + " seconds...")
            QtGui.QGuiApplication.processEvents()
            time.sleep(1)
        for masterRows in masterBusinessdFrame.index:
            masterData = masterBusinessdFrame['masterBusinessdFrame'][masterRows]
            for blRows in blDataFrame.index:
                blData = blDataFrame['blDataBusiness'][blRows]
                if masterData == blData:
                    # start comparison here --master--
                    masterBusinessColumns.fillna('', inplace=True)
                    blDataColumns.fillna('', inplace=True)
                    masterLicenseNumber = masterBusinessColumns.iloc[masterRows,1]
                    masterLicenseNumber = regEx.sub(r'\n', ' ', str(masterLicenseNumber))
                    masterLicensingAuthority = masterBusinessColumns.iloc[masterRows,3]
                    masterStateProvince = masterBusinessColumns.iloc[masterRows,4]
                    masterStatusPerCTAudit = masterBusinessColumns.iloc[masterRows,6]
                    if masterStatusPerCTAudit == "No Record" or masterStatusPerCTAudit == "Cannot Locate" or masterStatusPerCTAudit == "Expired" or masterStatusPerCTAudit == "Past Due" or masterStatusPerCTAudit == "Delinquent" or masterStatusPerCTAudit == "Suspended":
                        masterStatusPerCTAudit = "Inactive"  # PD feedback 12142019
                    masterRenewalDatePerCTAudit = masterBusinessColumns.iloc[masterRows,7]
                    if masterRenewalDatePerCTAudit == "N/A":
                        masterRenewalDatePerCTAudit = ""  # PD feedback 12142019
                    masterRenewalFrequencyPerCTAudit = masterBusinessColumns.iloc[masterRows,8]
                    if masterRenewalFrequencyPerCTAudit == "Annual":
                        masterRenewalFrequencyPerCTAudit = "1 Years"
                    if masterRenewalFrequencyPerCTAudit == "Biennial":
                        masterRenewalFrequencyPerCTAudit = "2 Years"
                    if masterRenewalFrequencyPerCTAudit == "Triennial":
                        masterRenewalFrequencyPerCTAudit = "3 Years"
                    #--BLHub--
                    blLicenseNumber = blDataColumns.iloc[blRows,2]
                    blLicenseAuthority = blDataColumns.iloc[blRows,11]
                    blStateProvince = blDataColumns.iloc[blRows,13]
                    blStatus = blDataColumns.iloc[blRows,7]
                    blRenewalDueDate = blDataColumns.iloc[blRows,26]
                    blRenewalType = blDataColumns.iloc[blRows,24] # optional for frequency used only
                    if masterRenewalFrequencyPerCTAudit == "Perpetual" or masterRenewalFrequencyPerCTAudit == "N/A":
                        if masterRenewalFrequencyPerCTAudit == blRenewalType:
                            masterRenewalFrequencyPerCTAudit_Other = "Match"
                        else:
                            masterRenewalFrequencyPerCTAudit_Other = "MisMatch"
                            logViewer.appendPlainText(str(masterData) + ": master Renewal Frequency Per CT Audit[" + str(masterRenewalFrequencyPerCTAudit) + "] not match with BL Hub Renewal Type[" + str(blRenewalType) + "]")
                            QtGui.QGuiApplication.processEvents()
                    blRecurrencePattern = blDataColumns.iloc[blRows,27]
                    # --Compare List--
                    if str(masterLicenseNumber) != blLicenseNumber:
                        logViewer.appendPlainText(str(masterData) + ": master License Number[" + str(masterLicenseNumber) + "] not match with BL Hub License Number[" + str(blLicenseNumber) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterLicensingAuthority) != str(blLicenseAuthority):
                        logViewer.appendPlainText(str(masterData) + ": master Licensing Authority[" + str(masterLicensingAuthority) + "] not match with BL Hub License Authority[" + str(blLicenseAuthority) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterStateProvince) != str(blStateProvince):
                        logViewer.appendPlainText(str(masterData) + ": master State/Province[" + str(masterStateProvince) + "] not match with BL Hub State/Province[" + str(blStateProvince) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterStatusPerCTAudit) != str(blStatus):
                        logViewer.appendPlainText(str(masterData) + ": master Status Per CT Audit[" + str(masterStatusPerCTAudit) + "] not match with BL Hub Status[" + str(blStatus) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterRenewalDatePerCTAudit) != str(blRenewalDueDate):
                        logViewer.appendPlainText(str(masterData) + ": master Renewal Date Per CT Audit[" + str(masterRenewalDatePerCTAudit) + "] not match with BL Hub Renewal Due Date[" + str(blRenewalDueDate) + "]")
                        QtGui.QGuiApplication.processEvents()
                    if str(masterRenewalFrequencyPerCTAudit) != str(blRecurrencePattern):
                        logViewer.appendPlainText(str(masterData) + ": master Renewal Frequency Per CT Audit[" + str(masterRenewalFrequencyPerCTAudit) + "] not match with Renewal Type[" + str(blRecurrencePattern) + "]")
                        QtGui.QGuiApplication.processEvents()
                    #if str(masterRenewalFrequencyPerCTAudit_Other) == "MisMatch":
                     #   logViewer.appendPlainText(str(masterData) + ": master Renewal Frequency Per CT Audit[" + str(masterRenewalFrequencyPerCTAudit) + "] not match with BlHub Renewal Type[" + str(blRenewalType) + "]")
                      #  QtGui.QGuiApplication.processEvents()
                    break
                # print(len(blDataFrame))
                if blRows == len(blDataFrame) - 1:
                    logViewer.appendPlainText(str(masterData) + " not found in BlHubList!")
                    QtGui.QGuiApplication.processEvents()

        # search for duplicates
        duplicateRowsDF = blDataFrame[blDataFrame.duplicated(['blDataBusiness'])]
        duplicateRowsDF = duplicateRowsDF.to_string()
        logViewer.appendPlainText("==============================================================")
        logViewer.appendPlainText("Found duplicate values: \n" + duplicateRowsDF)
        QtGui.QGuiApplication.processEvents()
        # --compare count of rows
        logViewer.appendPlainText("==============================================================")
        QtGui.QGuiApplication.processEvents()
        BlHubRowCounts = blDataFrame.shape[0]
        masterRowCounts = masterBusinessdFrame.shape[0]
        if BlHubRowCounts != masterRowCounts:
            logViewer.appendPlainText("\nRow Matching of Master Against BlHub:\nMaster count of rows:[" + str(
                masterRowCounts) + "] is not match with [" + str(BlHubRowCounts) + "]!")
            QtGui.QGuiApplication.processEvents()
    if contentSet == "E1 Comparison":
        rowStart = 1
        columnStart = 2,3
        if os.path.exists(tempPath + "statesValue"):
            os.remove(tempPath + "statesValue")
        masterColumns = pd.read_excel(masterPathText.text(), header=0, skiprows=1, ).reset_index(drop=True)
        E1Columns = pd.read_excel(blHubPathText.text(), header=0)
        dFrameMaster = pd.DataFrame(masterColumns)
        dFrameE1 = pd.DataFrame(E1Columns)
        masterConcatColumns = dFrameMaster[['Name of\nLicense Holder', 'Filing State', 'License Type']]
        masterConcatColumns = masterConcatColumns.replace(to_replace="AK", value="Alaska")
        masterConcatColumns = masterConcatColumns.replace(to_replace="AL", value="Alabama")
        masterConcatColumns = masterConcatColumns.replace(to_replace="AR", value="Arkansas")
        masterConcatColumns = masterConcatColumns.replace(to_replace="AZ", value="Arizona")
        masterConcatColumns = masterConcatColumns.replace(to_replace="CA", value="California")
        masterConcatColumns = masterConcatColumns.replace(to_replace="CO", value="Colorado")
        masterConcatColumns = masterConcatColumns.replace(to_replace="CT", value="Connecticut")
        masterConcatColumns = masterConcatColumns.replace(to_replace="DC", value="District of Columbia")
        masterConcatColumns = masterConcatColumns.replace(to_replace="DE", value="Delaware")
        masterConcatColumns = masterConcatColumns.replace(to_replace="FL", value="Florida")
        masterConcatColumns = masterConcatColumns.replace(to_replace="GA", value="Georgia")
        masterConcatColumns = masterConcatColumns.replace(to_replace="HI", value="Hawaii")
        masterConcatColumns = masterConcatColumns.replace(to_replace="IA", value="Iowa")
        masterConcatColumns = masterConcatColumns.replace(to_replace="ID", value="Idaho")
        masterConcatColumns = masterConcatColumns.replace(to_replace="IL", value="Illinois")
        masterConcatColumns = masterConcatColumns.replace(to_replace="IN", value="Indiana")
        masterConcatColumns = masterConcatColumns.replace(to_replace="KS", value="Kansas")
        masterConcatColumns = masterConcatColumns.replace(to_replace="KY", value="Kentucky")
        masterConcatColumns = masterConcatColumns.replace(to_replace="LA", value="Louisiana")
        masterConcatColumns = masterConcatColumns.replace(to_replace="MA", value="Massachusetts")
        masterConcatColumns = masterConcatColumns.replace(to_replace="MD", value="Maryland")
        masterConcatColumns = masterConcatColumns.replace(to_replace="ME", value="Maine")
        masterConcatColumns = masterConcatColumns.replace(to_replace="MI", value="Michigan")
        masterConcatColumns = masterConcatColumns.replace(to_replace="MN", value="Minnesota")
        masterConcatColumns = masterConcatColumns.replace(to_replace="MO", value="Missouri")
        masterConcatColumns = masterConcatColumns.replace(to_replace="MS", value="Mississippi")
        masterConcatColumns = masterConcatColumns.replace(to_replace="MT", value="Montana")
        masterConcatColumns = masterConcatColumns.replace(to_replace="NC", value="North Carolina")
        masterConcatColumns = masterConcatColumns.replace(to_replace="ND", value="North Dakota")
        masterConcatColumns = masterConcatColumns.replace(to_replace="NE", value="Nebraska")
        masterConcatColumns = masterConcatColumns.replace(to_replace="NH", value="New Hampshire")
        masterConcatColumns = masterConcatColumns.replace(to_replace="NJ", value="New Jersey")
        masterConcatColumns = masterConcatColumns.replace(to_replace="NM", value="New Mexico")
        masterConcatColumns = masterConcatColumns.replace(to_replace="NV", value="Nevada")
        masterConcatColumns = masterConcatColumns.replace(to_replace="NY", value="New York")
        masterConcatColumns = masterConcatColumns.replace(to_replace="OH", value="Ohio")
        masterConcatColumns = masterConcatColumns.replace(to_replace="OK", value="Oklahoma")
        masterConcatColumns = masterConcatColumns.replace(to_replace="OR", value="Oregon")
        masterConcatColumns = masterConcatColumns.replace(to_replace="PR", value="Puerto Rico")
        masterConcatColumns = masterConcatColumns.replace(to_replace="PA", value="Pennsylvania")
        masterConcatColumns = masterConcatColumns.replace(to_replace="RI", value="Rhode Island")
        masterConcatColumns = masterConcatColumns.replace(to_replace="SC", value="South Carolina")
        masterConcatColumns = masterConcatColumns.replace(to_replace="SD", value="South Dakota")
        masterConcatColumns = masterConcatColumns.replace(to_replace="TN", value="Tennessee")
        masterConcatColumns = masterConcatColumns.replace(to_replace="TX", value="Texas")
        masterConcatColumns = masterConcatColumns.replace(to_replace="UT", value="Utah")
        masterConcatColumns = masterConcatColumns.replace(to_replace="VA", value="Virginia")
        masterConcatColumns = masterConcatColumns.replace(to_replace="VT", value="Vermont")
        masterConcatColumns = masterConcatColumns.replace(to_replace="WA", value="Washington")
        masterConcatColumns = masterConcatColumns.replace(to_replace="WI", value="Wisconsin")
        masterConcatColumns = masterConcatColumns.replace(to_replace="WV", value="West Virginia")
        masterConcatColumns = masterConcatColumns.replace(to_replace="WY", value="Wyoming")
        E1ConcatColumns = dFrameE1[['Target']]
        masterConcatColumns['masterE1'] = masterConcatColumns['Name of\nLicense Holder'].str.cat(
            masterConcatColumns['Filing State'], sep=" - ")
        masterConcatColumns['masterConcatColumns'] = masterConcatColumns['masterE1'].str.cat(
            masterConcatColumns['License Type'], sep=" ")
        masterConcatColumns = masterConcatColumns[['masterConcatColumns']]
        for timer in reversed(range(1, 4)):
            logViewer.appendPlainText("Gathering data " + str(timer) + " seconds...")
            QtGui.QGuiApplication.processEvents()
            time.sleep(1)
        E1ConcatColumns = trim_all_columns(E1ConcatColumns)

        for masterRows in masterConcatColumns.index:
            masterData = masterConcatColumns['masterConcatColumns'][masterRows]
            for blRows in E1ConcatColumns.index:
                blData = E1ConcatColumns['Target'][blRows]
                if masterData == blData:
                    # logViewer.appendPlainText(str(masterData) + " found in BlHubList!")
                    break
                # print(len(blDataFrame))
                if blRows == len(E1ConcatColumns) - 1:
                    logViewer.appendPlainText(str(masterData) + " not found in E1 List!")
                    QtGui.QGuiApplication.processEvents()

        # search for duplicates
        duplicateRowsDF = masterConcatColumns[masterConcatColumns.duplicated(['masterConcatColumns'])]
        duplicateRowsDF = duplicateRowsDF.to_string()
        logViewer.appendPlainText("==============================================================")
        logViewer.appendPlainText("Found duplicate values: \n" + duplicateRowsDF)
        QtGui.QGuiApplication.processEvents()
        BlHubRowCounts = dFrameMaster.shape[0]
        masterRowCounts = dFrameE1.shape[0]
        logViewer.appendPlainText("==============================================================")
        if BlHubRowCounts != masterRowCounts:
            logViewer.appendPlainText("\nRow Matching of Master Against E1:\nMaster count of rows:[" + str(
                masterRowCounts) + "] is not match with [" + str(BlHubRowCounts) + "]!")
            QtGui.QGuiApplication.processEvents()

    logViewer.appendPlainText("\nDone Processing... Please see above logs...")
    QtGui.QGuiApplication.processEvents()
    now = datetime.now()
    now = now.microsecond
    read_ini_config.writeFileWrite(tempPath + "BLMSOnBoardingValidation" + str(now) + ".logs", logViewer.toPlainText())
    logViewer.appendPlainText("\nLogs also saved in " + tempPath)
    QtGui.QGuiApplication.processEvents()


def spellchecker(wrdtospellcheck):
    from spellchecker import SpellChecker
    spell = SpellChecker()
    words = spell.split_words(wrdtospellcheck)
    misspelled = spell.unknown(words)
    for word in misspelled:
        # Get the one `most likely` answer
        print(spell.correction(word))
        # Get a list of `likely` options
        print(spell.candidates(word))


def trim_all_columns(df):
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def readConfiguration():
    global masterPath, blHubPath, master, blHub, statesColumn
    global masterLicenseNumberColumn, masterLicensingAuthorityColumn, masterStateProvinceColumn, masterStatusPerCTAuditColumn
    global masterRenewalDatePerCTAuditColumn, masterRenewalFrequencyPerCTAuditColumn
    global blLicenseNumberColumn, blLicenseAuthorityColumn, blStateProvinceColumn, blStatusColumn, blRenewalDueDateColumn
    global blRenewalTypeColumn, blRecurrencePatternColumn
    if selectComboBox.currentText() == "Assumed Names":
        masterPath = read_ini_config.read_config("Assumed Names", "master Path")
        blHubPath = read_ini_config.read_config("Assumed Names", "BLHub Path")
        masterPathText.setText(masterPath)
        blHubPathText.setText(blHubPath)
        master = read_ini_config.read_config("Assumed Names", "master")
        blHub = read_ini_config.read_config("Assumed Names", "BLHub")
        masterLicenseNumberColumn = read_ini_config.read_config("Assumed Names", "masterLicenseNumber")
        masterLicensingAuthorityColumn = read_ini_config.read_config("Assumed Names", "masterLicensingAuthority")
        masterStateProvinceColumn = read_ini_config.read_config("Assumed Names", "masterStateProvince")
        masterStatusPerCTAuditColumn = read_ini_config.read_config("Assumed Names", "masterStatusPerCTAudit")
        masterRenewalDatePerCTAuditColumn = read_ini_config.read_config("Assumed Names", "masterRenewalDatePerCTAudit")
        masterRenewalFrequencyPerCTAuditColumn = read_ini_config.read_config("Assumed Names", "masterRenewalFrequencyPerCTAudit")
        blLicenseNumberColumn = read_ini_config.read_config("Assumed Names","blLicenseNumber")
        blLicenseAuthorityColumn = read_ini_config.read_config("Assumed Names", "blLicenseAuthority")
        blStateProvinceColumn = read_ini_config.read_config("Assumed Names", "blStateProvince")
        blStatusColumn = read_ini_config.read_config("Assumed Names", "blStatus")
        blRenewalDueDateColumn = read_ini_config.read_config("Assumed Names", "blRenewalDueDate")
        blRenewalTypeColumn = read_ini_config.read_config("Assumed Names", "blRenewalType")
        blRecurrencePatternColumn = read_ini_config.read_config("Assumed Names", "blRecurrencePattern")

    if selectComboBox.currentText() == "Business Licenses":
        masterPath = read_ini_config.read_config("Business Licenses", "master Path")
        blHubPath = read_ini_config.read_config("Business Licenses", "BLHub Path")
        masterPathText.setText(masterPath)
        blHubPathText.setText(blHubPath)
        master = read_ini_config.read_config("Business Licenses", "master")
        blHub = read_ini_config.read_config("Business Licenses", "BLHub")

    if selectComboBox.currentText() == "E1 Comparison":
        masterPath = read_ini_config.read_config("E1 Comparison", "master Path")
        blHubPath = read_ini_config.read_config("E1 Comparison", "BLHub Path")
        masterPathText.setText(masterPath)
        blHubPathText.setText(blHubPath)
        master = read_ini_config.read_config("E1 Comparison", "master")
        blHub = read_ini_config.read_config("E1 Comparison", "BLHub")
        statesColumn = read_ini_config.read_config("E1 Comparison", "StateColumn")
    return masterPath, blHubPath, master, blHub


def manualBrowsePathMaster():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(None, "Browse Master Excel File", masterPathText.text(),
                                              "Excel File (*.xlsx);;Excel File (*.xls)", options=options)
    if fileName:
        fileName = os.path.normpath(fileName)
        masterPathText.setText(fileName)


def manualBrowsePathBlHub():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(None, "Browse BLHub Excel File", blHubPathText.text(),
                                              "Excel File (*.xlsx);;Excel File (*.xls)", options=options)
    if fileName:
        fileName = os.path.normpath(fileName)
        blHubPathText.setText(fileName)


def showDialog(textMessage, messageTitle):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(str(textMessage))
    msg.setWindowTitle(messageTitle)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.exec_()
    return


# connect button to function
validateButton.clicked.connect(startValidation)
browseMasterPath.clicked.connect(manualBrowsePathMaster)
browseBlHubPath.clicked.connect(manualBrowsePathBlHub)
selectComboBox.currentTextChanged.connect(readConfiguration)

# read text path
readConfiguration()
masterPathText.setText(masterPath)
blHubPathText.setText(blHubPath)

# Show the window and run the app
win.show()
app.exec_()
