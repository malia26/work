from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient
from time import sleep
api_id = 2965455
api_hash = "3a82ff0f95a0550589e4d16ff999764b"


def enter(phones, group, link):
    for phone in phones:
        try:
            client = TelegramClient(phone, api_id, api_hash)
            client.connect()
            client(JoinChannelRequest(group))
            sleep(3)
            client(JoinChannelRequest(link))
            sleep(1)
            client.disconnect()
        except Exception as e:
            print(e)
            print(phone)
