import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from fake_useragent import UserAgent
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class scrapy:
    dataIndex = 0

    def __init__(self, path_settings, headers, useColumn):
        self.setPathSettings(path_settings)
        self.setRequestHeader(headers)
        self.setImportFile(useColumn)

    def setPathSettings(self, path_settings):
        self.path_settings = {
            "importDir": path_settings.get("importDir"),
            "importFile": path_settings.get("importFile"),
            "exportDir": path_settings.get("exportDir"),
            "exportFile": path_settings.get("exportFile")
        }

    def setRequestHeader(self,headers):
        self.headers = headers
        
    def setRandomUserAgent(self):
        user_agent = UserAgent()
        self.headers["user-agent"] = user_agent.random
        
    def setImportFile(self, useColumns=None):
        if self.path_settings["importFile"].split('.')[1] == 'xlsx':
            self.df = pd.DataFrame(pd.read_excel(
                self.path_settings["importDir"]+self.path_settings["importFile"], usecols=useColumns))
        else:
            self.df = pd.DataFrame(pd.read_csv(
                self.path_settings["importDir"]+self.path_settings["importFile"], usecols=useColumns))

    def setExportFile(self, exportColumn):
        i = 0
        self.excel_file = Workbook()
        self.sheet = self.excel_file.active
        for col in exportColumn:
            self.sheet[chr(65+i)+"1"] = col
            i += 1

    def sendRequest(self, url):
        try:
            self.res = requests.get(url, headers=self.headers, verify=False)
        except:
            raise ConnectionError(
                "第"+str(self.dataIndex)+"筆 " + self.df.at[self.dataIndex, '公司名稱']+" request失敗")
        else:
            if self.res.status_code != 200:
                raise ConnectionError(
                    "第"+str(self.dataIndex)+"筆 " + self.df.at[self.dataIndex, '公司名稱']+" request失敗")

    def parseResponse(self):
        self.res.encoding = "utf-8"
        self.soup = BeautifulSoup(self.res.text, "html.parser")