import requests, urllib, urllib2, cookielib, httplib
#from bs4 import BeautifulSoup

import time #for sleeping in between requests

import sys  #for cmd line args

# customized encyrpted database using simplecrypt
from credentialDB import *

#over-the-sholder pw protection 
# *** note only works when running in terminal NOT py shell *** 
from getpass import getpass

# emailAlerts.py holds functions for emailing users updates/alerts
from emailAlerts import *


# global consts for ems charts site #
URL = "www.emscharts.com/"
SCHEME = "https://"
DEFAULT_PAGE = "pub/default.cfm"
LOGIN_PAGE = "loginpage.cfm"
LOGIN_TARGET = 'pub/authx.asp'

# show requests
DEBUG = False


    ########## vvv loginAutomation vvv ##########
# attempt to log user in and return True/false, log
def runLogin(USR, PIN):
    # logging info for dubugging
    returnLog=""
    
    # items to be posted to the login form
    login_data = {
        'ambulance_cflogin_tag':'1',
        'k_username': USR,
        'k_password': PIN
    }    
    
    cj = cookielib.CookieJar()
    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    
    login_data = urllib.urlencode(login_data)
    ### build first request for authentication page ###
    request = urllib2.Request(SCHEME +  URL + LOGIN_TARGET, data=login_data)
    ## add request header information
    request.add_header("Accept",'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request.add_header("Origin",SCHEME+URL)
    request.add_header("Upgrade-Insecure-Requests",'1')
    request.add_header("User-Agent",'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
    request.add_header("Content-Type",'application/x-www-form-urlencoded')
    request.add_header("Referer",SCHEME+URL+DEFAULT_PAGE)
    # overload get method function 
    method = "POST"
    request.get_method = lambda: method    
    
    
    ### build request 2 for post-authentication, login page ###
    request2 = urllib2.Request(SCHEME +  URL + LOGIN_PAGE, data=login_data)
    ## add request header information
    request2.add_header("Accept",'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request2.add_header("Origin",SCHEME+URL)
    request2.add_header("Upgrade-Insecure-Requests",'1')
    request2.add_header("User-Agent",'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
    request2.add_header("Content-Type",'application/x-www-form-urlencoded')
    request2.add_header("Referer",SCHEME+URL+LOGIN_TARGET)
    # overload the get method function with a small anonymous function...
    method = "POST"
    request2.get_method = lambda: method     

    
    
    ## sumit requests to server ##
    resp = opener.open(request)
    time.sleep(3) # delays for 3 seconds
    resp = opener.open(request2)
    time.sleep(3) # delays for 3 seconds


    #httplib.HTTPConnection.debuglevel = 1

    if (DEBUG):
        print resp.url
        print resp.headers.dict
        
        print "\n===READ()===\n"

    
    output = resp.read()
    
    if (DEBUG):
        print output
        
    loggedIn = output.find('type="button" value="logout"')
    
    if (DEBUG):
        print "\n\nIs LoggedIn ="+str(loggedIn)  +"\n"
        
    
    if (not loggedIn == -1):
        return (True, returnLog)
    else:
        return (False, returnLog)
     
   ############ ^^^ loginAutomation ^^^ #############


   ######## vvv get info securely from user, preventing over-shoulder risks vvv ########
def getUserID():
    userID_A = ""
    userID_B = ""

    userID_A = getpass('Enter your userID: ')
    userID_B = getpass('Re-Enter your userID: ')     
    
    while (not userID_A == userID_B and (not userID_A == "") ):
        print "User IDs did not match. Please try again"
        userID_A = getpass('Enter your userID: ')
        userID_B = getpass('Re-Enter your userID: ')
    
    return userID_A
   
    
def getUserPW():
    userPW_A = ""
    userPW_B = ""

    userPW_A = getpass('Enter your user password: ')
    userPW_B = getpass('Re-Enter your user password: ')     
    
    while (not userPW_A == userPW_B and (not userPW_A == "") ):
        print "User passwords did not match. Please try again"
        userPW_A = getpass('Enter your user password: ')
        userPW_B = getpass('Re-Enter your user password: ')
    
    return userPW_A    
    
def getUserEmail():
    userEmail_A = ""
    userEmail_B = ""

    userEmail_A = getpass('Enter your email: ')
    userEmail_B = getpass('Re-Enter your email: ')     
    
    while (not userEmail_A == userEmail_B and (not userEmail_A == "") ):
        print "Emails did not match. Please try again"
        userEmail_A = getpass('Enter your email: ')
        userEmail_B = getpass('Re-Enter your email: ')
    
    return userEmail_A

    ###### ^^^ get info securely from user ^^^ ######
    
    
    
    
    #### MAIN ####
if __name__ == '__main__':
    # check if adding/modifying/removing user by cmd line args
    
    # normal, scheduled execution #
    if (len(sys.argv) == 2):
        #get db key
        key = sys.argv[1]
        
        #get all users from db
        (AllUsers, result) = returnAllUsers(key)
        if (not "Success" in result):
            print "database returnAllUsers(key) did not return properly:\n"+result
            sys.exit()
        
        if ("Warn" in result):
            print "database returnAllUsers(key) did returned with warning:\n"+result
            print "\nContinuing.."
            
            
        #run each user through auto-login
        for user in AllUsers:
            # Auto-Login & send user email alert 
            loggedin = runLogin(user['userID'], user['userPW'])
            if (loggedin):
                emailSuccess(user['userEmail'])
            else:
                emailFailure(user['userEmail'])
       
        sys.exit()
        
    
    # edit mode #
    if (len(sys.argv) == 3):
        print "command line args detected!"
        print "AutoLogin running in edit mode"
        print 'for usage, run with "help"'
        print "==============================="
        print
        
        key = sys.argv[1]


        if (sys.argv[2] == ("help")):
            print "Usage:"
            print "-run with only [KEY] as arguement for normal login of all users in db"
            print "-run with arguements: [KEY] 'add' --to add user to db of users"
            print "-run with arguements: [KEY] 'remove' --to remove user to db of users"
            print
            
        elif (sys.argv[2] == "add"):
            #add user if not already in db
            userID = getUserID()
            userPW = getUserPW()
            userEmail = getUserEmail()
            
            result=addNewUser(key, userID, userPW, userEmail)
            if ("Success" in result):
                print "User added succcessfully!"
            else:
                print "database addNewUser() did not return properly:\n"+result
        
        elif ( sys.argv[2] == "remove" ):
            #remove user if in db
            userID = getUserID()
            result = removeUser(key, userID)
            if ("Success" in result):
                print "User removed successfully!"
            else:
                print "database removeUser() did not return properly:\n"+result            
            
        else:
            #invalid arg
            print "invalid argument: "+sys.argv[2]
       
            
    else:
        #len(sys.argv) > 3 or < 2
        print "invalid number of arguments. see usage"
        print  
        print "Usage:"
        print "-run with only [KEY] as arguement for normal login of all users in db"
        print "-run with arguements: [KEY] 'add' --to add user to db of users"
        print "-run with arguements: [KEY] 'remove' --to remove user to db of users"