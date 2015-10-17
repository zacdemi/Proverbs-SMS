from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import config
from datetime import datetime
import random
import plivo
import smtplib

client = MongoClient()
db = client.bible
collection = db.bible
users = db.users
appname = "get proverbs"

def return_phone(user_id):
    user = users.find_one({"_id":ObjectId(user_id)})
    phone = user["Phone"]
    return phone

def return_id(phone):
    user = users.find_one({"Phone":phone})
    user_id = user["_id"]
    return user_id

def subscriber_count():
    count = users.find({"Subscribed":"Yes"}).count()
    return count

def adduser(phone):
    #generate new confirmation code
    confirmation = random.randrange(1000,5000)

    newuser = {"Phone":phone,"Confirmation":confirmation,"History":[],"Subscribed":"Not Yet"}
    #remove user if they already exist
    users.remove({"Phone":phone})
    users.insert(newuser)

def add_frequency(freq):
    pass
    #frequency = [i*1 for i in range(int(frequency))]

def subscribe_user(phone,action): #set action to Yes or No
    update = users.update({"Phone":phone},{"$set": {"Subscribed":action,"Date":datetime.now()}})
    try: 
        sendnotification(phone,action)
    except:
        pass
    return update

def userexist(phone):
    count = users.find({"Phone":phone,"Subscribed":"Yes"}).count()
    return count > 0

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

def userstatus(phone):
    user = users.find_one({"Phone":phone})
    status = user["Subscribed"]
    return status

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
    message =  line + " " + str(verse_id)
    return message

def sendtext(phone,message): #using Plivo
    # Your PLIVO_AUTH_ID and PLIVO_AUTH_TOKEN can be found
    # on your Plivo Dashboard https://manage.plivo.com/dashboard
    PLIVO_AUTH_ID = config.plivo_auth
    PLIVO_AUTH_TOKEN = config.plivo_token

    # Enter your Plivo phone number. This will show up on your caller ID
    plivo_number = config.plivo_number

    message_params = {
          'src':plivo_number,
          'dst': "1" + phone,
          'text':message,
        }
    p = plivo.RestAPI(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)
    print p.send_message(message_params)

def sendfirst(phone):
    message = ("The fear of the LORD is the beginning of knowledge; "
            "fools despise wisdom and instruction. 1:7") 
    sendtext(phone,message)

def sendconfirm(phone):
    user = users.find_one({"Phone":phone})   
    message = "This is your " + appname + " confirmation code " + str(user["Confirmation"])
    sendtext(phone,message)
   
def sendproverbs():
    today = datetime.strftime(datetime.today(),"%w")

    #loop through user database
    subscribers = users.find({"Subscribed":"Yes"}) 
    for each in subscribers:
        phone = each["Phone"]
        frequency = each["Frequency"]
        message = make_message(selectverse(phone))

        #send text
        if int(today) in frequency: 
            print message
            sendtext(phone,message)

#randomize member frequency
#run at the start of each week
def update_freq():
    subscribers = users.find({"Subscribed":"Yes"})
    for each in subscribers:
        phone = each["Phone"]
        freq = each["Frequency"]
        new_freq = random.sample(range(7),len(freq))
        users.update({"Phone":phone},{"$set":{"Frequency":new_freq}})

#convert distinct tags into tuples for checkboxes
def distincttag():
    #taglist = collection.distinct("Tags")
    taglist = ['anger','humility','joy','parenting','pride','speech','money','laziness','work','lust']
    
    tagtuple = []
    for x in taglist:
        count = collection.find({"Tags":x}).count()
        capital = x.capitalize()
        tag = x
        
        insert = (tag,capital + ' (' + str(count) + ')')
        tagtuple.append(insert)

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

#send text for free through gmail -AT&T only
def sendnotification(phone,status):
        #establish connection to gmail
        server = smtplib.SMTP( "smtp.gmail.com",587)
        server.starttls()
        server.login(config.email_username,config.email_password)
        count = str(subscriber_count())
        message = str(phone) + ' has ' + status  + '. current subscriber count is ' + count

        #send text
        server.sendmail('Wisdom',config.phone1 + '@mms.att.net',message)
        server.sendmail('Wisdom',config.phone2 + '@mms.att.net',message)



