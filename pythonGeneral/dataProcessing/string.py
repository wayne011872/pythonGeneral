import re
class reString:
    regex = ""
    def __init__(self,originStr):
        self.originStr = originStr
    def getNumberString(self):
        processStr = ""
        self.regex = re.compile(r"\d")
        processObj = self.regex.finditer(self.originStr)
        for chr in processObj:
            processStr+=chr.group()
        return processStr
    def deleteSpace(self):
        processStr = re.sub(r" ",r"",self.originStr)
        return processStr
    def deleteChar(self,deleteChar):
        processStr = re.sub(deleteChar,r"",self.originStr)
        return processStr
    def insertChar(self,insertIndex,insertChar):
        insertStrList = list(self.originStr)
        insertStrList.insert(insertIndex, insertChar)
        insertStrList = ''.join(insertStrList)
        return insertStrList

def InsertChar(insertStr, insertIndex, insertChar):
    insertStrList = list(insertStr)
    insertStrList.insert(insertIndex, insertChar)
    insertStrList = ''.join(insertStrList)
    return insertStrList

def deleteSpace(originStr):
    processStr = re.sub(r" ",r"",originStr)
    return processStr