import json

from lib.models import UserModel
from lib.proverbs import confirm_code

def create_user(event, context):
    data = json.loads(event['body'])

    user = UserModel(phone=data['phone'],
                     confirm=confirm_code())
    user.save()

    # create a response
    return {'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(dict(user))}
    

    
