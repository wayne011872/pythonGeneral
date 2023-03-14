import pymongo
import toml

class mon:
    def __init__(self,initFileAddress,databaseName=None,collectionName=None):
        config = toml.load(initFileAddress+"config.toml")
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
        findData = self.myCollection.find_one(data)
        return findData

    def findManyData(self, data):
        findData = self.myCollection.find(data)
        return findData

    def findAllData(self):
        findData = self.myCollection.find()
        return findData
    
    def findGeometryData(self,findCoordinate,findDistance):
        findDict = {}
        location = {}
        nearSphere = {}
        geometry = {}
        geometry["type"] = "Point"
        geometry["coordinates"] = findCoordinate
        nearSphere["$geometry"] = geometry
        nearSphere["$maxDistance"] = findDistance
        location["$nearSphere"] = nearSphere
        findDict["location"] = location
        findData = self.myCollection.find(findDict)
        return findData
    
    def updateOneData(self,findData,updateData):
        self.myCollection.update_one(findData,updateData)
        
    def updateManyData(self,findData,updateData):
        self.myCollection.update_many(findData,updateData)
    
    def deleteOneData(self,data):
        self.myCollection.delete_one(data)
    
    def deleteManyData(self,data):
        self.myCollection.delete_many(data)