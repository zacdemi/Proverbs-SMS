import json

from models import UserModel
from common import send_sms, confirm_code

def create_user(event, context):
    data = json.loads(event['body'])

    user = UserModel(phone=data['phone'], confirm=confirm_code())
    user.save()

    #send confirm code
    send_sms(data['phone'],confirm_code())


    # create a response
    return {'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(dict(user))}
