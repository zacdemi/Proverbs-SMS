import random
from datetime import datetime, timedelta, date
from pymongo import MongoClient
from bson.json_util import dumps

#given the freqency and proverb count return last proverb day
def runout_date(frequency,count):
    weeks = count/frequency.count() 
    d = date(2015,1,1)
    t = timedelta(weeks = weeks)
    n = d + t
    return n

#given a date return month week
#'first','second','third','fourth' or 'fifth'
def week_of_month(runout_date):
    first = datetime.monthrange(runout_date)[0]
    day = datetime.day.runoutdate
    
freq = [1,2,3,4]

#randomize member frequency
#run this at the start of each week
def update_freq(freq):
    new_freq = random.sample(range(7),len(freq))
    users = users.find({})
    for each in users:
        phone = users["Phone"]
        users.update({"Phone":phone},{"$set":{"Frequency":new_freq}})

    return new_freq

def addtag(book, chapter, verse, *args):
    Tags = [item.lower() for item in list(args)]
    collection.update(
        {'Book': book,'Chapter': chapter,'Verse': verse},
        {'$addToSet': {'Tags': {'$each': Tags}}})
    tagstatus = collection.find_one(
        {'Book': book,'Chapter': chapter,
        'Verse': verse}, {'_id': False})
    return dumps(tagstatus, indent=4)

def deletetag(book, chapter, verse, *args):
    Tags = [item.lower() for item in list(args)]
    collection.update(
        {'Book': book,'Chapter': chapter,'Verse': verse},
        {'$set': {'Tags': Tags}})
    tagstatus = collection.find_one(
        {'Book': book,'Chapter': chapter,'Verse': verse},
        {'_id': False})
    return dumps(tagstatus, indent=4)

def findtag(*args):
    Tags = list(args)
    results = []
    search = collection.find({'Tags': {'$in': Tags}}, {'_id': False})
    for each in search:
         results.append(each)
    return results