# Telegram Scraper and Adder Bot

This Telegram bot consists of two parts: a scraper bot and an adder bot. The scraper bot is responsible for scraping members from Telegram groups and saving them to CSV files, while the adder bot can add the scraped members to a target group or multiple groups at same time.

## Scraper Bot

The scraper bot is used to extract member details from Telegram groups and store them in CSV files for later use. To run the scraper bot, follow the steps below:

1. Install the required dependencies by running the following command:
pip install telethon

2. Create a Telegram app and obtain your API credentials (API ID and API Hash) by following the Telegram API documentation.

3. Update the `api_id`, `api_hash`, and `phone` variables in the `scraper_bot.py` file with your API credentials and phone number.

4. Run the scraper bot using the following command:
python tel_scraper.py


5. Enter your Telegram account confirmation code when prompted.

6. The scraper bot will display a list of available groups. Enter the number corresponding to the group you want to scrape members from.

7. The bot will start scraping the members and save them to a CSV file named `members.csv`.

## Adder Bot

The adder bot is used to add the scraped members to a target group. To run the adder bot, follow the steps below:

1. Make sure you have successfully run the scraper bot and have the `members.csv` file available.

2. Update the `api_id`, `api_hash`, and `phone` variables in the `adder_bot.py` file with your API credentials and phone number.

3. Run the adder bot using the following command:
python adder_bot.py


4. Enter your Telegram account confirmation code when prompted.

5. The adder bot will display a list of available CSV files. Enter the numbers (separated by commas) corresponding to the files you want to add members from.

6. The bot will prompt you to select a target group to add the members to. Enter the number corresponding to the desired group.

7. The bot will start adding the members to the selected group, with a delay of 60 to 180 seconds between each addition to avoid flooding Telegram's servers.

## Important Note

- Make sure to keep your API credentials (API ID and API Hash) confidential and do not share them with anyone.

- Use the bots responsibly and ensure compliance with Telegram's terms of service and guidelines.

- The bots may take some time to complete the operations, especially when dealing with a large number of members. Be patient and let the bots run until they finish.

- Remember to give credits to the original author, `@Levi Chinecherem C or Semantic Dev`, if you use any parts of this code.

- Feel free to customize the code according to your specific needs and requirements.

For any issues or questions, please contact `@SemanticDev` on Telegram.

Happy scraping and adding!
