import pymongo
import configparser

class mon:
    def __init__(self,initFileAddress,databaseName=None,collectionName=None):
        config = configparser.ConfigParser()
        config.read(initFileAddress+"config.ini")
        self.myClient = pymongo.MongoClient("mongodb://"+config['mongodb']['server']+":"+config['mongodb']['port']+"/")
        if databaseName:
            self.myDB = self.myClient[databaseName]
        else:
            self.myDB = self.myClient[config['mongodb']['database']]
        
        if collectionName:
            self.myCollection = self.myDB[collectionName]
        else:
            self.myCollection = self.myDB[config['mongodb']['collection']]

    def insertOneData(self, data):
        self.myCollection.insert_one(data)

    def insertManyData(self, data):
        self.myCollection.insert_many(data)

    def findOneData(self, data):
        self.myCollection.find_one(data)

    def findManyData(self, data):
        self.myCollection.find(data)

    def findAllData(self):
        self.myCollection.find()
    
    def updateOneData(self,data):
        self.myCollection.update_one(data)
        
    def updateManyData(self,data):
        self.myCollection.update_many(data)
    
    def deleteOneData(self,data):
        self.myCollection.delete_one(data)
    
    def deleteManyData(self,data):
        self.myCollection.delete_many(data)