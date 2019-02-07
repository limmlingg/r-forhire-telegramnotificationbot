import praw
import telegram
import pdb
import re
import os

####################################################################
# Telegram bot parts                                               #
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/ #
####################################################################

# TODO
def startTelegramBot():

    telegram_bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    return telegram_bot

    # # Create the EventHandler and pass it the bot's token
    # updater = Updater(TELEGRAM_BOT_TOKEN)
    
    # return updater;


######################
# Reddit bot methods #
######################

def startRedditBot(): 
    reddit_bot = praw.Reddit('bot')

    reddit_bot.login(REDDIT_USERNAME, REDDIT_PASS)

    return reddit_bot


########
# Main #
########

def main():

    telegram_bot = startTelegramBot()
    reddit_bot = startRedditBot()

    # Get the file with the time of the most recent post checked
    if not os.path.isfile("last_post_time.txt"):
        last_post_time = []
    else:
        with open("last_post_time.txt", "r") as f:
            last_post_time = f.read()

    most_recent_time = last_post_time

    # Pull the newest entries from r/forhire
    subreddit = reddit_bot.subreddit('forhire')
    for submission in subreddit.new(limit=20):
        #print(submission.title)

        # Get time of most recent post in this search
        if (submission.created_utc > most_recent_time):
            most_recent_time = submission.created_utc

        # Stop looping once it reaches a submission older than the last checked post
        if submission.created_utc <= last_post_time:
            break

        # Check that the post is a [HIRING] post
        if re.match('\[hiring\]', submission.title, re.IGNORECASE):
            # Check if the hiring post contains the specified keywords
            # Regex searches for "video editor" or "video editing". ?: to make the parentheses not a capturing group
            if re.search('video\s(?:editor|editing)', submission.selftext, re.IGNORECASE):
                # Send a telegram message if it contains
                telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=submission.permalink)

    # Write most recent time to file
    with open("last_post_time.txt", "w") as f:
        f.write(most_recent_time)

if __name__ == '__main__':
    main()