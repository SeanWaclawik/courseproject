# simple crypt credential db 


#    public-return a list of credentials (client must supply key)
#        returnAllUsers(key)
#          returns list [of 3 dictionary items {userID:**, userPW:**, userEmail} ... ]
#          AND returns String of Log (will contain "Success" iff successful)

#    public-add new user to db (client must supply key)
#         addNewUser(key, userID, userPass, userEmail)
#           return string (log) will include "Success" iff added, "Warn" / "Error" otherwise

#    public-remove user from db (client must supply key)
#        removeUser(key, userID)
#           return string (log) will include "Success" iff removed, "Warn" / "Error" otherwise

#    private-open/create db in same directory
#    verifyDB()  :  returns True if db exists and accesable, False otherwise



from simplecrypt import encrypt, decrypt


# this is the permenant name of AutoLogin credential data base
dbName = "AutoLoginData.db"


# example simple crypt usage:
#plaintext= "credentials"

#ciphertext = encrypt('key', plaintext)
#print ciphertext
#plaintext = decrypt('key', ciphertext)



### open/create db in same directory
def verifyDB():
    db = open(dbName, 'ab')
    if (not db):
        return False
        # "Error: could not open or create db in append mode"+"\n\t"+dbName
    db.close()
    return True
        


###    add new user to db (client must supply key) 
def addNewUser( key, userID, userPass, userEmail ):
    # return string contains log info about success/failure/warnings adding user
    returnLog = ""

    newUserData = userID+"\n"+userPass+"\n"+userEmail+"\n"
    
    # verify db exists or try to create it)
    if not verifyDB():
        returnLog += "Error: could not open or create db"+"\n\t"+dbName+"\n"
        return returnLog
    
    # get every line from file, decypt
    db = open(dbName, 'rb')
    if (not db):
        returnLog += "Error: could not open db in read mode"+"\n\t"+dbName+"\n"
        db.close()
        return returnLog
        
    cryptData = db.read()
    if (not cryptData == ""):
        Data = decrypt(key, cryptData)
        
        # check if user already exists
        if (userID in Data):
            returnLog += "Warn: userID already in db\n--no data added\n"
            db.close()
            return returnLog
        else:
            Data = Data + newUserData
    
    else: #no data yet in db
        returnLog += "info: no pre-existing data in db\n"
        Data = newUserData

    # encyrpt back to database
    cyrptData = encrypt(key, Data)


    # check the db, clear it, & write back
    db = open(dbName, 'wb')
    if (not db):
        returnLog += "Error: could not open db in write mode"+"\n\t"+dbName+"\n"
        db.close()
        return returnLog
    
    db.write(cyrptData)
    db.close()
    
    returnLog += "Success\n"

    return returnLog






###    remove user from db (client must supply key) 
def removeUser(key, userID):
    # return string contains log info about success/failure/warnings removing user
    returnLog = ""

        
    # verify db exists or try to create it
    if not verifyDB():
        returnLog += "Error: could not open or create db"+"\n\t"+dbName+"\n"
        return returnLog
    
    # get every line from file, decypt
    db = open(dbName, 'rb')
    if (not db):
        returnLog += "Error: could not open db in read mode"+"\n\t"+dbName+"\n"
        db.close()
        return returnLog
        
    cryptData = db.read()
    if (not cryptData == ""):
        Data = decrypt(key, cryptData)
        
        # check if user exists
        if (userID in Data):
            # remove id, pw, email upto and including '\n'
            start = Data.index(userID)
            end = Data.find("\n", start)+1 # id
            end = Data.find("\n", end)+1   # pw
            end = Data.find("\n", end)+1   # email
            Data = Data[:start]+Data[end:]
            
            
            
        # if not no user to remove    
        else:
            returnLog += "Warn: userID not in db\n--no user to remove\n"
            db.close()
            return returnLog            
    
    else: #no data in db
        returnLog += "Warn: no existing data in db\n"
        db.close()
        return returnLog



    # encyrpt back to database
    cyrptData = encrypt(key, Data)


    # check the db, clear it, & write back
    db = open(dbName, 'wb')
    if (not db):
        returnLog += "Error: could not open db in write mode"+"\n\t"+dbName+"\n"
        db.close()
        return returnLog
    
    db.write(cyrptData)
    db.close()
    
    returnLog += "Success\n"

    return returnLog







###    read all users from db (client must supply key) 
###    returns tuple of returnData and returnLog
def returnAllUsers(key):
    # list of dicts to hold info
    returnData = []
    
    # return string contains log info about success/failure/warnings
    returnLog = ""    
    
    # verify db exists or try to create it)
    if not verifyDB():
        returnLog += "Error: could not open or create db"+"\n\t"+dbName+"\n"
        return (returnData, returnLog)
    
    # get every line from file, decypt
    db = open(dbName, 'rb')
    if (not db):
        returnLog += "Error: could not open db in read mode"+"\n\t"+dbName+"\n"
        db.close()
        return (returnData, returnLog)
        
    cryptData = db.read()
    db.close()
    
    if (cryptData == ""):
        returnLog += "Warn: empty db\n"
        db.close()
        return (returnData, returnLog)
    
    
    Data = decrypt(key, cryptData)
    
    # split at new-lines
    Data = Data.split('\n')
    
    if (not len(Data) % 3 == 1):
        returnLog += "Error: len(Data) should always == 1 mod 3. db len is multiple of 3 plus 1\n"
        return (returnData, returnLog)
    
    i=0
    while (i < len(Data)-1):
        userDict={}
        for j in range (3):
            # case userID
            if (j==0):
                userDict['userID']=Data[i]
            # case userPW
            if (j==1):
                userDict['userPW']=Data[i]
            # case userEmail
            if (j==2):
                userDict['userEmail']=Data[i]
            i+=1

        returnData.append(userDict)
    
    
    returnLog += "Success"
    
    return (returnData, returnLog)

