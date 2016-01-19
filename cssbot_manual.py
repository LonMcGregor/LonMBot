import praw
import json
import fileinput
import html
import string

#statics
UPS_LOC = 'up'
SUBREDDIT = 'MonarchyOfEquestria'

#globals
r = praw.Reddit(user_agent = "praw:lonmcgregor.cssmanager:v1.1;(by /u/LonMcGregor)")
style = ""

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
    print("UID, without preceding id-t2_ tag:")
    uid = input()
    print("New Name:")
    name = input()
    if(isValidName(name)):
        style = getStyle()
        appendToStyle(uid, name)
    if(needsUpdating == 1):
        print("Style updating... ")
        r.set_stylesheet(SUBREDDIT, style)        
        
login()
run()