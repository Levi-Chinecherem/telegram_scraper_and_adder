# (c) @Levi-Chinecherem
# Telegram: http://t.me/@SemanticDev
# Please give me credits if you use any codes from here.

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel
import csv
import time
import random

api_id = 123456
api_hash = 'YOUR_API_HASH'
phone = '+111111111111'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

csv_file = input("Enter the CSV file path: ")

groups = []
with open(csv_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        group = {
            'title': row[4],
            'id': int(row[5])
        }
        if group not in groups:
            groups.append(group)

if len(groups) == 0:
    print("No groups found in the CSV file. Please run the scraper bot first to scrape members.")
    exit(1)

print("Choose a group to add members:")
for i, group in enumerate(groups):
    print(f"{i}. {group['title']}")

g_index = input("Enter a number: ")
target_group = groups[int(g_index)]

members = []
with open(csv_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        member = {
            'username': row[0],
            'id': int(row[1]),
            'access_hash': int(row[2]),
            'name': row[3]
        }
        members.append(member)

print("Adding members to the group...")
for member in members:
    try:
        user_to_add = InputPeerChannel(member['id'], member['access_hash'])
        client(InviteToChannelRequest(target_group['id'], [user_to_add]))
        print(f"Added {member['name']} to {target_group['title']}")
        time.sleep(random.randint(5, 15))
    except Exception as e:
        print(f"Failed to add {member['name']} to {target_group['title']}: {e}")

print("Adding members completed.")
