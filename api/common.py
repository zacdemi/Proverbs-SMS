import os
import random
import requests

def send_sms(phone, message):
    """
    send a sms message using Plivo API
    phone number

    phone: string
    message: string
    """
    auth_id = os.environ['PLIVO_AUTH_ID']
    auth_token = os.environ['PLIVO_AUTH_TOKEN']
    plivo_phone = os.environ['PLIVO_PHONE']

    url = f'https://api.plivo.com/v1/Account/{auth_id}/Message/'
    post = {'src':plivo_phone, 'dst':phone,'text':message}
    headers = {'Content-type': 'application/json'}

    r = requests.post(url, json=post, auth=(auth_id, auth_token), headers=headers)
    print(r.status_code)

def confirm_code():
    """ 
    return a random 4 digit number as a string
    """
    code = random.randrange(1000,9999)
    return str(code)
