import pandas as pd
import pythonGeneral.dataProcessing.string as pds
import os

class df_data:
    def __init__(self, path_settings=None, useColumns=None):
        if path_settings:
            self.set_pathSettings(path_settings=path_settings)
        else:
            self.path_settings["importFile"] = ""
        self.setImportDf(useColumns)

    def set_pathSettings(self, path_settings):
        self.path_settings = {
            "importDir": path_settings.get("importDir"),
            "importFile": path_settings.get("importFile"),
            "exportDir": path_settings.get("exportDir"),
            "exportFile": path_settings.get("exportFile")
        }
    
    def setExportFile(self,exportFile):
        self.path_settings["exportFile"] = exportFile

    def set_mergeSettings(self, mergeSettings):
        self. mergeSettings = {
            "mergeOnList": mergeSettings.get("mergeOnList"),
            "dropList": mergeSettings.get("dropList"),
            "renameDict": mergeSettings.get("renameDict")
        }

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

    def dropStringNotInData(self, inString, column):
        self.df = self.df[self.df[column].str.contains(inString)]
        
    def dropStringInData(self,dropString,column):
        self.df = self.df[~self.df[column].str.contains(dropString,na=False)]
    
    def cutData(self, start=None, end=None):
        self.df = self.df.iloc[start:end, :]

    def sortData(self, sortColumns):
        self.df = self.df.sort_values(by=sortColumns)

    def deleteDuplicate(self, deleteDupColumn: str):
        self.df.drop_duplicates(subset=deleteDupColumn, inplace=True)

    def deleteNone(self, deleteNoneColumn: str):
        self.df.dropna(axis=0, subset=deleteNoneColumn, inplace=True)
    
    def getNone(self, getNoneColumn):
        self.df = self.df[self.df[getNoneColumn].isnull()]
    
    def processData(self, deleteNoneColumn, deleteDupColumn, sortColumns):
        self.df.dropna(axis=0, subset=deleteNoneColumn, inplace=True)
        self.df.drop_duplicates(subset=deleteDupColumn, inplace=True)
        self.df = self.df.sort_values(by=sortColumns)

    def substituteOneString(self, beSubString: str, subString: str, subColumn: str):
        for i in range(len(self.df)):
            d = pds.reString(str(self.df.at[i, subColumn]))
            d.substituteOneString(beSubString,subString)
            self.df.at[i, subColumn] = d.processStr
    
    def substituteManyString(self,subDict:dict,subColumn:str):
        for i in range(len(self.df)):
            d = pds.reString(str(self.df.at[i, subColumn]))
            d.substituteManyString(subDict)
            self.df.at[i, subColumn] = d.processStr
    
    def processRegexString(self,regex:str,processColumn:str):
        for i in range(len(self.df)):
            d = pds.reString(str(self.df.at[i, processColumn]))
            d.processRegexString(regex)
            self.df.at[i, processColumn] = d.processStr
    
    def deleteSpaceChar(self,deleteStrColumn):
        for i in range(len(self.df)):
            d = pds.reString(str(self.df.at[i,deleteStrColumn]))
            d.deleteSpace()
            self.df.at[i,deleteStrColumn] = d.processStr

    def dataToTPSData(self):
        for i in range(len(self.df)):
            self.df.at[i, '資本額'] = (str(self.df.at[i, '資本額']) + ", 工廠登記編號:"+str(self.df.at[i, '工廠登記編號'])
                                    + ",產業類別:"+str(self.df.at[i, '產業類別'])+",主要產品:"+str(self.df.at[i, '主要產品'])+",網址:"+str(self.df.at[i, '網址']))

    def mergeData(self, dfRight, mergeSettings):
        self.set_mergeSettings(mergeSettings=mergeSettings)
        self.df = self.df.merge(
            right=dfRight.df,
            how="left",
            on=self.mergeSettings["mergeOnList"],
            indicator=True
        )
        if self.mergeSettings["dropList"] != None:
            self.df.drop(self.mergeSettings["dropList"], axis=1, inplace=True)
        if self.mergeSettings["renameDict"] != None:
            self.df.rename(columns=self.mergeSettings["renameDict"], inplace=True)

    def toFile(self):
        if self.path_settings["exportFile"].split('.')[1] == 'csv':
            self.df.to_csv(
                self.path_settings["exportDir"]+self.path_settings["exportFile"], index=False, encoding='utf-8-sig')
        elif self.path_settings["exportFile"].split('.')[1] == 'xlsx':
            self.df.to_excel(
                self.path_settings["exportDir"]+self.path_settings["exportFile"], index=False)
        else:
            print("沒有設定exportFile或exportDir")


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