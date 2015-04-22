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
