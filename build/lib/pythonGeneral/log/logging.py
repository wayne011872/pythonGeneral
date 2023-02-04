import logging
import os

class myLogger:
    def __init__(self,logName,logLevel,logDir):
        os.makedirs(logDir,exist_ok=True)
        logPath = logDir+logName+".txt"
        self.logger = logging.getLogger(logName)
        self.setLoggerLevel(logLevel)
        self.fileHandler = logging.FileHandler(logPath,mode='w')
        self.setHandlerLevel(logLevel)
        self.allFormatter = logging.Formatter(
            "%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
        self.fileHandler.setFormatter(self.allFormatter)
        self.logger.addHandler(self.fileHandler)
    
    def setLoggerLevel(self,logLevel):
        if logLevel == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif logLevel == "INFO":
            self.logger.setLevel(logging.INFO)
        elif logLevel == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif logLevel == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif logLevel == "CRITICAL":
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.DEBUG)
    def setHandlerLevel(self,logLevel):
        if logLevel == "DEBUG":
            self.fileHandler.setLevel(logging.DEBUG)
        elif logLevel == "INFO":
            self.fileHandler.setLevel(logging.INFO)
        elif logLevel == "WARNING":
            self.fileHandler.setLevel(logging.WARNING)
        elif logLevel == "ERROR":
            self.fileHandler.setLevel(logging.ERROR)
        elif logLevel == "CRITICAL":
            self.fileHandler.setLevel(logging.CRITICAL)
        else:
            self.fileHandler.setLevel(logging.DEBUG)