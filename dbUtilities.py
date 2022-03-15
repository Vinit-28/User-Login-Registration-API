# Importing the required modules #
from os import stat
from random import random
import pymongo
import dns
import bcrypt
import secrets
import string


# class to perfrom operations in database #
class dbUtilities():

    # Initializing Database Configs #
    def __init__(self, connectionString):
        self.connectionString = connectionString 
        self.mongoDbClientObject = pymongo.MongoClient(connectionString)
        self.dbObject = None
        self.collectionObject = None
        self.dbsInfo = {}


    # Making database # 
    def makeDB(self, dbName):
        self.dbsInfo[dbName] = {}
        self.setDBObject(dbName = dbName)


    # Making Collections of a Database #
    def makeDBcollections(self, dbName, collectionNamesWithDescription):

        # Iterating through all the collections #
        for collection in collectionNamesWithDescription:
            self.dbsInfo[dbName][collection] = collectionNamesWithDescription[collection]


    # Pointing to new database #
    def setDBObject(self, dbName):
        self.dbObject = self.mongoDbClientObject[dbName]


    # Pointing to new collection in the current database #
    def setCollectionObject(self, collectionName):
        self.collectionObject = self.dbObject[collectionName]


    # Find whether the userName is registered or not #
    def isUserRegistered(self, userName):
        self.setDBObject(dbName = "myApp")
        self.setCollectionObject(collectionName = "registeredUsers")

        result = self.collectionObject.count_documents({
            "userName" : userName
        })

        return result == 1

    
    # Registering the user #
    def registerUser(self, userDetails):

        # If the userName does not exits in the database #
        if not self.isUserRegistered(userName = userDetails['userName']):
            userDetails['password'] = bcrypt.hashpw(userDetails['password'].encode('utf-8'), bcrypt.gensalt())
            self.collectionObject.insert_one(userDetails)
            self.setCollectionObject("userStatus")
            self.collectionObject.insert_one({
                "userName" : userDetails['userName'],
                "status" : "Offline",
                "sessionId" : ""
            })
            return True
        # If the userName already exists in the database #
        else:
            return False
    

    # Getting all the registered users #
    def getRegisteredAllUsers(self):
        self.setDBObject(dbName = "myApp")
        self.setCollectionObject(collectionName = "registeredUsers")
        queryResult = self.collectionObject.find({}, {"_id":False, "password":False})
        userIndex = 1
        allUsers = {}
        # Iterating through all the registered users #
        for user in queryResult:
            allUsers[userIndex] = user
            userIndex += 1
        
        return allUsers


    # Trying to logging in user #
    def loginUser(self, userDetails):

        self.setDBObject(dbName = "myApp")
        self.setCollectionObject(collectionName = "registeredUsers")    
        queryResult = self.collectionObject.find({"userName" : userDetails['userName']}, {"_id":False, "password":True})

        # If user Exists with the specified userName #
        try:
            user = queryResult.next()
            # If Password Matches #
            if bcrypt.checkpw(userDetails['password'].encode('utf-8'), user['password']):
                self.changeUserStatus(userName = userDetails['userName'], status = True) # Changing user status #
                return True
            else:
                return False
        except :
            return False
    

    # Changing User Status (Online/Offline) #
    def changeUserStatus(self, userName, status):  
        self.setDBObject(dbName = "myApp")
        self.setCollectionObject(collectionName = "userStatus")   

        # Updating the User Status to Online #
        if status:
            randomId = self.generateRandomId()
            print("Random Id = >", randomId)
            self.collectionObject.update_one({"userName" : userName}, {"$set" : {"status" : "Online", "sessionId" : randomId}})
        # Updating the User Status to Offline #
        else:
            self.collectionObject.update_one({"userName" : userName}, {"$set":{"status" : "Offline", "sessionId" : ""}})



    # Generating a random string/Id #
    def generateRandomId(self, idLen = 10):
        # generating random Id (String) 
        randomId = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(idLen))
        return str(randomId)


    # Find whether the user is logged in or not #
    def isUserLoggedIn(self, userName):
        self.setDBObject(dbName = "myApp")
        self.setCollectionObject(collectionName = "userStatus")   
        result = self.collectionObject.count_documents({
            "userName" : userName,
            "status" : "Online"
        })

        return result == 1


    # Trying to logout the user #
    def logoutUser(self, userName):

        if self.isUserLoggedIn(userName = userName):
            self.changeUserStatus(userName = userName, status = False)
            return True
        else:
            return False
    
    
    # Reseting User's Password #
    def resetUserPassword(self, userDetails):
        
        self.setDBObject(dbName = "myApp")
        self.setCollectionObject(collectionName = "registeredUsers")    
        queryResult = self.collectionObject.find({"userName" : userDetails['userName']}, {"_id":False, "password":True})

        # If user Exists with the specified userName #
        try:
            user = queryResult.next()
            print(user, "\n\n\n")
            # If Password Matches #
            if bcrypt.checkpw(userDetails['oldPassword'].encode('utf-8'), user['password']):
                userDetails['newPassword'] = bcrypt.hashpw(userDetails['newPassword'].encode('utf-8'), bcrypt.gensalt())
                self.collectionObject.update_one({"userName" : userDetails['userName']}, {"$set":{"password" : userDetails['newPassword']}})
                return True
            else:
                return False
        except:
            return False
        
        
