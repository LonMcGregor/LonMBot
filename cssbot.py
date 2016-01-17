import praw
import json
import fileinput
import html
import string

#statics
READ_LIMIT = 5
LOG_LOC = 'readmessages'
UPS_LOC = 'up'
SUBREDDIT = 'MonarchyOfEquestria'
TRIGGER = 'MakeName'

#globals
r = praw.Reddit(user_agent = "praw:lonmcgregor.cssmanager:v1;(by /u/LonMcGregor)")
currentlog = []
style = ""
needsUpdating = 0

#log me in function
def login():
    pos = 0;
    ups = ["", ""]
    with fileinput.input(files=(UPS_LOC)) as f:
        for line in f:
            word = line.rstrip('\n')
            ups[pos] = word
            pos = pos + 1
    print("Logging in...")
    r.login(ups[0], ups[1])
    print("Logged in.")
    
#clear the log to just last READ_LIMIT entries
def cleanLog():
    print("Cleaning Log")
    counter = 0
    lines = []
    with fileinput.input(files=(LOG_LOC)) as f:
        for line in f:
            if (counter == 0):
                (0==0)
            else:
                if (counter <= READ_LIMIT):
                    lines.append(line)
            counter = counter + 1
    f = open(LOG_LOC, 'w')
    for str in lines:
        f.write(str)
    f.close()
    readLog()

#read the log into list
def readLog():
    global currentlog
    print("Reading log")
    currentlog = []
    with fileinput.input(files=(LOG_LOC)) as f:
        for line in f:
            currentlog.append(line.rstrip('\n'))

#write a new entry to the log
def writeToLog(log):
    print("Logging... "+ log)
    cleanLog()
    f = open(LOG_LOC, 'a')
    f.write(log+'\n')
    f.close()
    readLog()
    
#return the last READ_LIMIT mod mails
def getModMail():
    print("Getting modmail")
    modreddit = r.get_subreddit(SUBREDDIT)
    return r.get_mod_mail(modreddit, limit=READ_LIMIT)
    
#return the SUBREDDIT's style
def getStyle():
    print("Getting stylesheet")
    return html.unescape(r.get_stylesheet(SUBREDDIT)['stylesheet'])

#helper function: does an iterable contain an item
def contains(list, item):
    try:
        list.index(item)
        return True
    except ValueError:
        return False
    
#check a message and act upon if necessary
def handleMsg(message):
    messageid = message.id
    print("Handling message "+messageid)
    if(not contains(currentlog, messageid)):
        if(message.subject == TRIGGER):
            if(isValidName(message.body)):
                appendToStyle(message.author.id, message.body)
                message.reply("Done!")
            else:
                message.reply("Please send a new message with a valid name. [contains a-z, A-Z, 0-9 and spaces only, less than 30 characters long]")
        writeToLog(messageid)
    else:
        print("Message previously handled")
        
#check if a new name is valid
def isValidName(name):
    name = name.lower()
    if(len(name)>30):
        return False
    for i in range(0, len(name)):
    #for each character in name
        if (not contains(string.ascii_letters, name[i])):
        #if it is not one of letter
            if (not contains(string.digits, name[i])):
            #if it is not one of number
                if(not name[i] == " "):
                #if not space
                    return False
                    #return false
    #return true
    return True

#add a new name to the style
def appendToStyle(userid, username):
    global style
    global needsUpdating
    print("Prepping style append for: "+userid+" to "+username)
    style = style + '\n    .id-t2_' + userid + ':before { content: "' + username + '"; }\n'
    style = style + '    .id-t2_' + userid + ':link {color: rgba(0,0,0,0); font-size: 0px; }\n'
    needsUpdating = 1
    
#run the bot
def run():
    global style
    global mail
    style = getStyle()
    mail = getModMail()
    print("Checking modmail")
    for msg in mail:
        handleMsg(msg)
    if(needsUpdating == 1):
        print("Style updating... ")
        r.set_stylesheet(SUBREDDIT, style)        
        
            
readLog()
login()
run()