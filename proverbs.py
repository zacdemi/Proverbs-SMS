from pymongo import MongoClient
from bson.json_util import dumps
import config
from datetime import datetime
import random
import smtplib

client = MongoClient()
db = client.bible
collection = db.bible
users = db.users
carrier_list = {'AT&T':'@mms.att.net','Verizon':'@vtext.com','Sprint':'@messaging.sprintpcs.com'}
appname = "Proverbs-SMS"

def adduser(phone,carrier,taglist,frequency):
    count = users.find({"Phone":phone}).count()
    #generate new confirmation code
    confirmation = random.randrange(1000,5000)

    frequency = [i*1 for i in range(int(frequency))]

    newuser = {"Phone":phone,"Carrier":carrier,"Tags":taglist,
                "Confirmation":confirmation,"Frequency":frequency,"History":[]}
    #remove user if they already existed
    users.remove({"Phone":phone})
    users.insert(newuser)

def subscribe_user(phone,action): #set action to Yes or No
    update = users.update({"Phone":phone},{"$set": {"Subscribed":action,"Date":datetime.now()}})
    return update

def update_user(phone,taglist,frequency):
    frequency = [i*1 for i in range(int(frequency))]
    update = users.update({"Phone":phone},{"$set": {"Tags":taglist,"Frequency":frequency,"History":[]}})
    return update

def checkconfirm(phone,confirmation):
    user = users.find_one({"Phone":phone})
    try:
        return user['Confirmation'] == confirmation
    except:
        return False

def userexist(phone):
    count = users.find({"Phone":phone,"Subscribed":"Yes"}).count()
    return count > 0

#finds a random proverb using only tags the user has selected
def findrandom(taglist):
    taglist = taglist
    count = collection.find(
        {"Book":"Proverbs","Tags":{"$in":taglist}}).count()
    #use random number to find random document
    randomverse = collection.find(
        {"Book":"Proverbs","Tags":{"$in":taglist}})[random.randrange(count)]
    t = str(randomverse["Chapter"]) + ":" + str(randomverse["Verse"])
    return  t


#uses findrandom until a verse is found that doesn't exist in history.
def selectverse(phone):
    user = users.find_one({"Phone":phone})   
    taglist = user["Tags"]
    history = user["History"]
    max_amount = collection.find(
        {"Book":"Proverbs","Tags":{"$in":taglist}}).count()

    count = 0
    while True:
        verse_id = findrandom(taglist)
        #verse already sent
        if verse_id not in history:
            push_new(phone,verse_id)
            break
        #all verses have been sent
        if count >= max_amount:
            verse_id = pop_new(phone)
            break

        count = count + 1
        print count
    return verse_id

#adds new verse to end of history array
def push_new(phone,verse_id):
    users.update({"Phone":phone},{"$push":{"History":verse_id}})

#user has used all tags
#uses oldest proverb and moves it to beginning of array
def pop_new(phone):
    #finds oldest proverb from history
    oldest = users.find_one({"Phone":phone},{"History":{"$slice":1}})
    oldest = str(oldest["History"]).strip("'[u]'")
    #remove oldest provberb from history
    users.update({"Phone":phone},{"$pop":{"History":-1}}) 
    #append oldest proverb to end of history array
    users.update({"Phone":phone},{"$push":{"History":oldest}})
    return oldest 

def make_message(verse_id):
    chapter = int(verse_id.split(":")[0])
    verse = int(verse_id.split(":")[1])

    proverb = collection.find_one({"Book":"Proverbs","Chapter":chapter,"Verse":verse})
    line = proverb["Line"]
    message =  line + " " + str(chapter) + " " + str(verse)
    #gmail won't send colons
    message = message.replace(":",";")
    return message

def sendconfirm(phone):
    #establish a connection with gmail
    server = smtplib.SMTP( "smtp.gmail.com",587)
    server.starttls()
    server.login(config.username,config.password)

    user = users.find_one({"Phone":phone})   
    carrier = user["Carrier"]
    address = str(phone) + carrier_list[carrier]
    #two confirm texts are sent
    if userexist(phone):
        message = ("The fear of the LORD is the beginning of knowledge; " 
                   "fools despise wisdom and instruction. 1 7")
    else:
        message = "This is your " + appname + " confirmation code " + str(user["Confirmation"])
    #send text
    server.sendmail('Wisdom',address,message)

def sendproverbs():
    #establish connection to gmail
    server = smtplib.SMTP( "smtp.gmail.com",587)
    server.starttls()
    server.login(config.username,config.password)

    today = datetime.strftime(datetime.today(),"%w")

    #loop through user database
    subscribers = users.find({"Test":"Yes"}) 
    for each in subscribers:
        phone = each["Phone"]
        carrier = each["Carrier"]
        tags = each["Tags"]
        frequency = each["Frequency"]
        address = str(phone) + carrier_list[carrier]
        message = make_message(selectverse(phone))

        #send text
        if int(today) in frequency: 
            server.sendmail('Wisdom',address,message)
       
#convert distinct tags into tuples for checkboxes
def distincttag():
    taglist = collection.distinct("Tags")
    tagtuple = [(x, x.capitalize()) for x in taglist]
    tagtuple = sorted(tagtuple)
    return tagtuple

def verse_length():
    for verse in collection.find({"Book":"Proverbs"}):
        if len(verse["Line"]) >= 160:
            print verse["Line"]

def proverbs_clock():
    t = datetime.time(datetime.now())
    hour =  t.hour
    minute = t.minute

    count = collection.find({"Book":"Proverbs","Chapter":hour,"Verse":minute}).count()
    proverb = collection.find_one({"Book":"Proverbs","Chapter":hour,"Verse":minute},{"_id":False})

    if count == 1:
        return proverb["Line"] + ' ' + str(proverb["Chapter"]) + ':' + str(proverb["Verse"])
    else:
        return "There is no Proverb " + str(hour) + ":" + str(minute)

def findtag(*args):
    Tags = list(args)
    results = []
    search = collection.find({'Tags': {'$in': Tags}}, {'_id': False})
    for each in search:
         results.append(each)
    return results 
