# (c) @Levi-Chinecherem
# Telegram: http://t.me/@SemanticDev
# Please give me credits if you use any codes from here.

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import os

api_id = 'YOUR_API_ID'   # Enter Your 7 Digit Telegram API ID.
api_hash = 'YOUR_API_HASH'   # Enter Your 32 Character API Hash
phone = 'YOUR_PHONE_NUMBER'   # Enter Your Mobile Number With Country Code.
client = TelegramClient(phone, api_id, api_hash)


async def main():
    await client.send_message('me', 'Hello!')


SLEEP_TIME_1 = 100
SLEEP_TIME_2 = 100

with client:
    client.loop.run_until_complete(main())

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the confirmation code: '))

# Get a list of all CSV files in the current directory
csv_files = [file for file in os.listdir() if file.endswith('.csv')]

if len(csv_files) == 0:
    print("No CSV files found in the current directory. Please run the scraper bot first to generate CSV files.")
    sys.exit()

# Prompt the user to select one or multiple CSV files
print("Available CSV files:")
for i, file in enumerate(csv_files):
    print(f"{i+1}. {file}")

file_numbers = input("Enter the numbers of the CSV files to add members (separated by commas): ")
file_indexes = map(int, file_numbers.split(","))
selected_files = [csv_files[index - 1] for index in file_indexes]

users = []
for selected_file in selected_files:
    with open(selected_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {
                'username': row[0],
                'id': int(row[1]),
                'access_hash': int(row[2]),
                'name': row[3],
                'group': row[4],
                'group_id': int(row[5])
            }
            users.append(user)

chats = []
last_date = None
chunk_size = 900
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

if len(groups) == 0:
    print("No groups found. Please join a group first.")
    sys.exit()

print('Choose a group to add members: ')
for i, group in enumerate(groups):
    print(str(i) + '- ' + group.title)

g_index = input("Enter the number: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        time.sleep(60)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting for 60-180 Seconds...")
        time.sleep(random.randrange(60, 181))
    except PeerFloodError:
        print("Getting Flood Error from Telegram. Script is stopping now. Please try again after some time.")
        print("Waiting {} seconds".format(SLEEP_TIME_2))
        time.sleep(SLEEP_TIME_2)
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping...")
        print("Waiting for 5 Seconds...")
        time.sleep(random.randrange(0, 5))
    except:
        traceback.print_exc()
        print("Unexpected Error!")
        continue
