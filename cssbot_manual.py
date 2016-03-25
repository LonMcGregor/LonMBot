import praw
import json
import fileinput
import html
import string

#statics
UPS_LOC = 'up'
SUBREDDIT = 'MonarchyOfEquestria'
ACCENTED = 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝßàáâãäåæçèéêëìíîïðñòóôõöùúûüýÿŒœŠšŸŽž'

#globals
r = praw.Reddit(user_agent = "praw:lonmcgregor.cssmanager:v1.2;(by /u/LonMcGregor)")
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
    r.login(ups[0], ups[1], disable_warning=True)
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
        if (not contains(string.ascii_letters, name[i])):
            if (not contains(string.digits, name[i])):
                if (not contains(ACCENTED, name[i])):
                    if(not name[i] == " "):
                        return False
    return True

#add a new name to the style
def appendToStyle(realid, newname):
    global style
    global needsUpdating
    print("Prepping style append for: "+realid+" to "+newname)
    style = style + '\n    .id-' + realid + ':before { content: "' + newname + '"; }\n'
    style = style + '    .id-' + realid + ':link {color: rgba(0,0,0,0); font-size: 0px; }\n'
    needsUpdating = True
    
#run the bot
def run():
    global style
    global needsUpdating
    needsUpdating = False
    print("Real username:")
    uid = input()
    user = r.get_redditor(uid)
    realid = user.fullname
    print("New Name:")
    name = input()
    if(isValidName(name)):
        style = getStyle()
        appendToStyle(realid, name)
    if(needsUpdating):
        print("Style updating... ")
        r.set_stylesheet(SUBREDDIT, style)
    else:
        print("Invalid New Name")
        
login()
run()
print("Exiting...")