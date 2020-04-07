import configparser
import os


def read_config(section, value):
    base_path = os.getcwd()
    parser = configparser.ConfigParser()
    parser.read(base_path + '\\CTCOB17 - BLMS On-Boarding Validation.ini')
    # print(parser.get(section, value))
    return parser.get(section, value)


def readFile(rPath):
    r_file = open(rPath, "r", encoding='utf8')  #"r"
    rslt_rFile = r_file.read()
    r_file.close()
    return rslt_rFile


def readLinesOfFile(rPath, Filename):
    r_file = open(rPath + Filename, "r", encoding='utf8')  #"r"
    rslt_rFile = r_file.readlines()
    r_file.close()
    return rslt_rFile


def writeFile(wPath, textContent):
    w_File = open(wPath, "a+", encoding='utf8')  # "a+"
    rslt_wFile = w_File.write(str(textContent))
    w_File.close()
    return


def writeFileWrite(wPath, textContent):
    w_File = open(wPath, "w", encoding='utf8')  # "w"
    rslt_wFile = w_File.write(str(textContent))
    w_File.close()
    return

