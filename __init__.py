# Importing the required modules #
from dbUtilities import dbUtilities
from flask import Flask, request, jsonify
from urllib.parse import quote_plus 


# Making Connection to the Database #
dbUserName = quote_plus("username")
dbPassword = quote_plus("password")
connectionString = ("mongodb+srv://%s:%s@thebookslibrary.elqki.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" % (dbUserName, dbPassword))
dbUtility = dbUtilities(connectionString = connectionString)
dbName = "myApp"
dbCollectionsWithDescription = {
    "registeredUsers" : "Will keep the record of Registered Users",
    "userStatus" : "Will store the user status"
}

dbUtility.makeDB(dbName = dbName)
dbUtility.makeDBcollections(dbName = dbName, collectionNamesWithDescription = dbCollectionsWithDescription)