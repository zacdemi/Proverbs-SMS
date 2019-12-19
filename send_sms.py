import plivo
import config

client = plivo.RestClient(config.PLIVO_AUTH_ID,config.PLIVO_AUTH_TOKEN)
message_created = client.messages.create(
    src=config.plivo_number,
    dst='16108361870',
    text='Hello, world!'
)
