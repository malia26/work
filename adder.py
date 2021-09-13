from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
import configparser
import csv
import datetime
from time import sleep
api_id = 2965455
api_hash = "3a82ff0f95a0550589e4d16ff999764b"

# phone = "+996558885367"

SLEEP_TIME = 30


def join_group(phone, group_title, link, n, rule):

    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    # if not client.is_user_authorized():
    #     client.send_code_request(phone)
    #     client.sign_in(phone, input('Enter the code: '))
    # ////////////////////

    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    print('From Which Group Yow Want To Scrap A Members:')
    i = 0
    for g in groups:
        print(g.username, group_title)
        if g.username == group_title:
            break
        i += 1

    print('Fetching Members...')
    target_group = ""
    try:
        target_group = groups[i]
        print(target_group.title)
        print("!!!!!!!!!!")
    except Exception as e:
        print(e)
        print(len(groups), i)
        client.disconnect()

    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving In file...')
    # Enter your file name.
    with open("Scrapped.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash',
                         'name', 'group', 'group id', "status"])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            if str(user.status).startswith('UserStatusRecently'):
                status = "recently"
            elif str(user.status).startswith('UserStatusOnline'):
                status = "online"
            else:
                try:
                    status = user.status.was_online.strftime(
                        '%Y-%m-%d %H:%M:%S')
                except:
                    status = ""

            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash,
                             name, target_group.title, target_group.id, status])
    print('Members scraped successfully.......')
    # /////////////////////
    input_file = "Scrapped.csv"
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        if rule == "0":
            print(1)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)

        elif rule == "1":
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                status = row[6]

                if status == "recently":
                    users.append(user)
        elif rule == "2":
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                status = row[6]
                if status == "online":
                    users.append(user)
        elif rule == "3":
            data = input("Input date: ")
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                status = row[6]
                try:
                    status = datetime.datetime.strptime(
                        status, '%Y-%m-%d %H:%M:%S').day
                    if str(status) == data:
                        users.append(user)
                except:
                    pass
        elif rule == "4":
            data = input("Input date: ")
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                status = row[6]
                try:
                    status = datetime.datetime.strptime(
                        status, '%Y-%m-%d %H:%M:%S').day
                    if str(status) == data:
                        users.append(user)
                except:
                    if status == "recently":
                        users.append(user)
                    if status == "online":
                        users.append(user)
    num = 0
    cutted_users = users[n:]
    channel = client.get_entity(link)
    for i in range(len(cutted_users)):
        if num % 45 == 0 and num != 0:
            print("changing account")
            client.disconect()
            return n
        try:
            client(InviteToChannelRequest(
                channel,
                [cutted_users[i]['id']]
            ))
            sleep(SLEEP_TIME)
            i += 1
            num += 1
            n += 1
            print(n)
        except UserPrivacyRestrictedError:
            i += 1
        except Exception as e:
            print(e)
            client.disconect()
            return n
