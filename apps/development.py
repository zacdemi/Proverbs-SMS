from datetime import datetime, timedelta, date


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
    
    

import random

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

print "test daily"
print update_freq([0,1,2,3,4,5,6])
print "test 5x week"
print update_freq([0,1,2,3,4,5])
print "test 4x week"
print update_freq([0,1,2,3])
print "test 3x week"
print update_freq([0,1,2])
print "test 2x week"
print update_freq([0,1])
print "test 1x week"
print update_freq([0])
