import pandas as pd
import os
import re

class df_data:
    def __init__(self, path_settings, useColumns=None):
        self.set_pathSettings(path_settings=path_settings)
        self.setImportDf(useColumns)

    def set_pathSettings(self, path_settings):
        self.path_settings = {
            "importDir": path_settings.get("importDir"),
            "importFile": path_settings.get("importFile"),
            "exportDir": path_settings.get("exportDir"),
            "exportFile": path_settings.get("exportFile")
        }

    def set_mergeSettings(self, mergeSettings):
        mergeSettings = {
            "mergeOnList": mergeSettings.get("mergeOnList"),
            "dropList": mergeSettings.get("dropList"),
            "renameDict": mergeSettings.get("renameDict"),
        }
        return mergeSettings

    def setImportDf(self, useColumns):
        if self.path_settings["importFile"].split('.')[1] == 'xlsx':
            self.df = pd.DataFrame(pd.read_excel(
                self.path_settings["importDir"]+self.path_settings["importFile"], usecols=useColumns))
        elif self.path_settings["importFile"].split('.')[1] == 'csv':
            self.df = pd.DataFrame(pd.read_csv(
                self.path_settings["importDir"]+self.path_settings["importFile"], usecols=useColumns))
        else:
            self.df = pd.DataFrame(columns=useColumns)

    def setData(self, df):
        self.df = df

    def stringNotInData(self, inString, column):
        self.df = self.df[self.df[column].str.contains(inString)]
        self.toFile()

    def cutData(self, start=None, end=None):
        self.df = self.df.iloc[start:end, :]
        self.toFile()

    def sortData(self, sortColumns):
        self.df = self.df.sort_values(by=sortColumns)
        self.toFile()

    def deleteDuplicate(self, deleteDupColumn: str):
        self.df.drop_duplicates(subset=deleteDupColumn, inplace=True)
        self.toFile()

    def deleteNone(self, deleteNoneColumn: str):
        self.df.dropna(axis=0, subset=deleteNoneColumn, inplace=True)
        self.toFile()

    def processData(self, deleteNoneColumn, deleteDupColumn, sortColumns):
        self.df.dropna(axis=0, subset=deleteNoneColumn, inplace=True)
        self.df.drop_duplicates(subset=deleteDupColumn, inplace=True)
        self.df = self.df.sort_values(by=sortColumns)
        self.toFile()

    def substituteData(self, oriString: str, subString: str, subColumn: str):
        for i in range(len(self.df)):
            d = re.sub(oriString, subString, str(self.df.at[i, subColumn]))
            self.df.at[i, subColumn] = d
        self.toFile()

    def dataToTPSData(self):
        for i in range(len(self.df)):
            self.df.at[i, '資本額'] = (str(self.df.at[i, '資本額']) + ", 工廠登記編號:"+str(self.df.at[i, '工廠登記編號'])
                                    + ",產業類別:"+str(self.df.at[i, '產業類別'])+",主要產品:"+str(self.df.at[i, '主要產品'])+",網址:"+str(self.df.at[i, '網址']))
        self.toFile()

    def mergeData(self, dfRight, mergeSettings):
        mergeSettings = self.set_mergeSettings(mergeSettings=mergeSettings)
        self.df = self.df.merge(
            right=dfRight.df,
            how="left",
            on=mergeSettings["mergeOnList"],
            indicator=True
        )
        if mergeSettings["dropList"] != None:
            self.df.drop(mergeSettings["dropList"], axis=1, inplace=True)
        if mergeSettings["renameDict"] != None:
            self.df.rename(columns=mergeSettings["renameDict"], inplace=True)
        self.toFile()

    def getNone(self, getNoneColumn):
        self.df = self.df[self.df[getNoneColumn].isnull()]
        self.toFile()

    def toFile(self):
        if self.path_settings["exportFile"].split('.')[1] == 'csv':
            self.df.to_csv(
                self.path_settings["exportDir"]+self.path_settings["exportFile"], index=False, encoding='utf-8-sig')
        else:
            self.df.to_excel(
                self.path_settings["exportDir"]+self.path_settings["exportFile"], index=False)


def concatDirData(importDir, exportFile):
    dfTotal = pd.DataFrame()
    for importFile in os.listdir(importDir):
        data = df_data({"importDir": importDir,
                        "importFile": importFile,
                        "exportDir": importDir,
                        "exportFile": exportFile})
        dfTotal = pd.concat([dfTotal, data.df])
    dfTotal.to_excel(importDir+exportFile, index=False)


def concatFileData(exportPath, *concatDf):
    dfTotal = pd.DataFrame()
    for df in concatDf:
        dfTotal = pd.concat([dfTotal, df])
    dfTotal.to_excel(exportPath, index=False)


def cutDirData(importDir, start, end):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"("+start+"-"+end+").xlsx"})
        df.cutData(start, end)
        df.toFile()


def sortDirData(importDir, sortColumns):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(排地址).xlsx"})
        df.sortData(sortColumns)
        df.toFile()


def deleteDirDuplicate(importDir, deleteDupColumn):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(去重複資料).xlsx"})
        df.deleteDuplicate(deleteDupColumn)
        df.toFile()


def deleteDirNone(importDir, deleteNoneColumn):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(去空白資料).xlsx"})
        df.deleteNone(deleteNoneColumn)
        df.toFile()


def getDirNone(importDir, getNoneColumn):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(抓空白資料).xlsx"})
        df.getNone(getNoneColumn)
        df.toFile()


def processDirData(importDir, deleteNoneColumn, deleteDupColumn, sortColumns):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(全處理).xlsx"})
        df.processData(deleteNoneColumn, deleteDupColumn, sortColumns)
        df.toFile()


def substituteDirData(importDir, oriString, subString, subColumn):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"("+oriString+'to'+subString+").xlsx"})
        df.substituteData(oriString, subString, subColumn)
        df.toFile()


def dirDataToTPSData(importDir):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(TPS處理).xlsx"})
        df.dataToTPSData()
        df.toFile()


def mergeDirData(importDir, dfLeft, mergeSettings):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(合併資料).xlsx"})
        df.mergeData(dfLeft, mergeSettings)
        df.toFile()


def stringNotInDirData(importDir, inString, columns):
    for importFile in os.listdir(importDir):
        df = df_data({"importDir": importDir,
                      "importFile": importFile,
                      "exportDir": importDir,
                      "exportFile": importFile.split('.')[0]+"(取"+inString+").xlsx"})
        df.stringNotInData(inString, columns)
        df.toFile()
