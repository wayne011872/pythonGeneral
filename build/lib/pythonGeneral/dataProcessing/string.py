import re
numSubDict = {
    '零': '0', '一': '1', '二': '2', '兩': '2', '三': '3',
    '四': '4', '五': '5', '六': '6', '七': '7', '八': '8',
    '九': '9', '〇': '0', '○': '0', '○': '0', '０': '0', '１': '1',
    '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7',
    '８': '8', '９': '9', '壹': '1', '貳': '2', '參': '3', '肆': '4',
    '伍': '5', '陆': '6', '柒': '7', '捌': '8', '玖': '9'
}


class reString:
    regex = ""

    def __init__(self, originStr):
        self.originStr = originStr
        self.processStr = originStr

    def getNumberString(self):
        processStr = ""
        self.regex = re.compile(r"\d")
        processObj = self.regex.finditer(self.processStr)
        for chr in processObj:
            processStr += chr.group()
        self.processStr = processStr

    def deleteSpace(self):
        self.processStr = re.sub(r" ", r"", self.processStr)

    def deleteString(self, deleteStr):
        self.processStr = re.sub(deleteStr, r"", self.processStr)

    def deleteOneChar(self, deleteChar: str):
        self.processStr = re.sub(deleteChar, r"", self.processStr)

    def deleteManyChar(self, deleteCharList: list):
        for deleteChar in deleteCharList:
            self.processStr = re.sub(deleteChar, r"", self.processStr)

    def insertChar(self, insertIndex: int, insertChar: str):
        insertStrList = list(self.processStr)
        insertStrList.insert(insertIndex, insertChar)
        insertStrList = "".join(insertStrList)
        self.processStr = insertStrList

    def substituteManyString(self, subDict: dict):
        for subChar in subDict:
            self.processStr = re.sub(
                subChar, subDict[subChar], self.processStr)

    def substituteOneString(self, beSubString: str, subString: str):
        self.processStr = re.sub(beSubString, subString, self.processStr)

    def processRegexString(self, regex: str):
        processStr = ""
        self.regex = re.compile(regex)
        processObj = self.regex.finditer(self.processStr)
        for chr in processObj:
            processStr += chr.group()
        self.processStr = processStr
    
    def turnChiNumberToNumber(self):
        self.substituteManyString(numSubDict)
            
    def getOriginString(self):
        return self.originStr

    def getProcessString(self):
        return self.processStr


def InsertChar(insertStr, insertIndex, insertChar):
    insertStrList = list(insertStr)
    insertStrList.insert(insertIndex, insertChar)
    insertStrList = ''.join(insertStrList)
    return insertStrList


def deleteSpace(originStr):
    processStr = re.sub(r" ", r"", originStr)
    return processStr
