from telethon.sync import TelegramClient
import csv
import time
import random

# Replace the values with your own API credentials
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'

# Connect to Telegram client
with TelegramClient('session_name', api_id, api_hash) as client:
    # Log in to your account
    client.start(phone_number)

    print("Logged in successfully.")

    # Ask the user to provide the CSV file name
    csv_filename = input("Enter the CSV file name (with extension) containing the scraped members: ")

    try:
        # Read the scraped members from the CSV file
        with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            members_to_add = list(reader)

        # Get a list of all the groups you are a member of
        groups = []
        for dialog in client.iter_dialogs():
            if dialog.is_group:
                groups.append(dialog)

        # Print the list of groups
        print("Available groups:")
        for i, group in enumerate(groups):
            print(f"{i+1}. {group.title}")

        # Ask the user to select one or more groups
        selected_groups = []
        group_numbers = input("Enter the numbers of the groups to add members (separated by commas): ")
        group_indexes = map(int, group_numbers.split(","))
        for index in group_indexes:
            if 1 <= index <= len(groups):
                selected_groups.append(groups[index - 1])

        # Add members to the selected groups
        added_count = 0
        for member in members_to_add:
            try:
                user_id = int(member[1])  # Assuming User ID is in the second column
                for group in selected_groups:
                    client(InviteToChannelRequest(group, [user_id]))
                    added_count += 1
                    delay = random.randint(5, 15)
                    print(f"Added member {added_count}, {user_id} to group '{group.title}'. Waiting for {delay} seconds...")
                    time.sleep(delay)
            except ValueError:
                print(f"Invalid User ID: {member[1]}")

        print(f"\nAdded {added_count} members to the selected groups successfully.")
    except FileNotFoundError:
        print(f"CSV file {csv_filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
