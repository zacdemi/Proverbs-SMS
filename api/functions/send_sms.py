import plivo

def send_sms(event, context):
    data = json.loads(event['body'])

    client = plivo.RestClient(os.environ.get('PLIVO_AUTH_ID'), os.environ.get('PLIVO_AUTH_TOKEN'))
    response = client.messages.create(
        src=os.environ.get('PLIVO_NUMBER'),
        dst=data['phone'],
        text=data['message'],
     )

    return(response)
