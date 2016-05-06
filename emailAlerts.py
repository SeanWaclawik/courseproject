# emailAlerts 
#
#  REQUIRES: "serverEmailAccount.txt" with email on first line and pw on second
#
#     has 2 methods which send user an email reporting success or failure
#
#  emailSuccess(userEmail)
#  emailFailure(userEmail)


import smtplib

#create an SMTP object for connection with email server
#Must allow 'less secure access' in gmail

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()



def getServerInfo():
    serverEmail = ""
    serverpw = ""    

    serverInfo = open("serverEmailAccount.txt", "r")
    
    if not serverInfo:
        print "ERROR: emailAlerts REQUIRES: 'serverEmailAccount.txt' with email on first line and pw on second"
        print "Email alerts will not work"
    
    else:
        serverEmail = serverInfo.readline()
        serverpw = serverInfo.readline()
    serverInfo.close()
    
    return (serverEmail, serverpw)



def emailSuccess(userEmail):
    # get login info
    (serverEmail, serverpw) = getServerInfo()
    
    #log in on server side
    server.login(serverEmail, serverpw)
    
    #Make and send email
    msg = "\r\n".join([
      "From: "+serverEmail,
      "To: "+userEmail,
      "Subject: AutoLogin",
      "",
      "AutoLogin has SUCCESSFULLY logged you in!"
      ])
    server.sendmail(serverEmail, userEmail, msg)
    
    
    
def emailFailure(userEmail):
    # get login info
    (serverEmail, serverpw) = getServerInfo()    
    #log in on server side
    server.login(serverEmail, serverpw)
    
    #Make and send email
    msg = "\r\n".join([
      "From: "+serverEmail,
      "To: "+userEmail,
      "Subject: AutoLogin ERROR",
      "",
      "AutoLogin has attempted to log you in but was unable to. \nPlease login manually. \nRespond to this email with your user ID and AutoLogin will look into this error."
      ])
    server.sendmail(serverEmail, userEmail, msg)

