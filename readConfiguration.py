import configparser
import read_ini_config


def readConfiguration(selectComboBox, masterPathText, blHubPathText):
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