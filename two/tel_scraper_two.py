# (c) @Levi-Chinecherem
# Telegram: http://t.me/@SemanticDev
# Please give me credits if you use any codes from here.

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = '+234 YOUR_PHONE_NUMBER'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Choose a group to scrape members from:')
for i, group in enumerate(groups):
    print(f"{i}. {group.title}")

g_index = input("Enter a number: ")
target_group = groups[int(g_index)]

print('Fetching Members...')
all_participants = client.get_participants(target_group, aggressive=True)

print('Saving in file...')
csv_filename = f"{target_group.title}_members.csv"
with open(csv_filename, "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
    for user in all_participants:
        username = user.username if user.username else ""
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

print(f"Members scraped successfully. Saved to {csv_filename}.")
