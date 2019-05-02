import feedparser   # Parses Reddit RSS feed
import discord      # Discord bot integration
import asyncio      # Delay between background task subsequent calls

SUBS_TO_CHECK = ['']                                # Subs to find users from
SUBS_TO_CATCH = ['']                                # Subs to match users against
CHECK_TIMER = 300                                   # Delay between subsequent checks
NUM_RECENT_USERS = 5                                # Checks the __ most recent posters in SUBS_TO_CHECK
UUID_TO_PING = ""                                   # Pings user when match found, if empty, will not ping
CHANNEL_ID = 0                                      # Channel ID to send updates to
BOT_TOKEN = ''                                      # Discord bot token


# UserData object to collate information on a get request
class UserData:
    def __init__(self, post, post_link, post_author):
        self.post = post
        self.post_link = post_link
        self.post_author = post_author


# DiscordBot object
class DiscordBot(discord.Client):
    # Initializes background polling task
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_check = self.loop.create_task(self.poll_check_users())

    # Login status + presence flair
    async def on_ready(self):
        print('Logged in as', self.user)
        await self.change_presence(activity=discord.Game(name='Investigating...'))

    # Polls for user participation in listed subreddits, sends message if found
    async def poll_check_users(self):
        await self.wait_until_ready()
        while not self.is_closed():
            user_data_list = get_recent_users()
            for user_data in user_data_list:
                if user_in_subreddit(user_data):
                    print("found match, sending message")
                    await self.send_message(user_data)
            await asyncio.sleep(CHECK_TIMER)

    async def send_message(self, user_data):
        channel = self.get_channel(CHANNEL_ID)
        if UUID_TO_PING == "":
            await channel.send(user_data.post + " by " + user_data.post_author + " (" + user_data.post_link + ")")
        else:
            await channel.send("<@" + UUID_TO_PING + "> || " + user_data.post + " by " + user_data.post_author +
                               " (" + user_data.post_link + ")")


# Gets a list of the 5 most recent users from each subreddit in SUBS_TO_CHECK
# INPUT: (none)
# OUTPUT: 2D array of UserData objects
def get_recent_users():
    recent_posters = []
    for subreddit in SUBS_TO_CHECK:
        post_feed = (feedparser.parse("https://www.reddit.com/r/" + subreddit + "/new/.rss"))['entries']
        for i in range(NUM_RECENT_USERS):
            post = post_feed[i]['title']
            post_link = post_feed[i]['link']
            post_author = post_feed[i]['author']
            user_data = UserData(post, post_link, post_author)
            recent_posters.append(user_data)
    return recent_posters


# Returns whether a user has recently participated in one of the subreddits in SUBS_TO_CHECK
# INPUT: UserData object
# OUTPUT: Boolean;
#   True if user participated in a subreddit list, otherwise False
def user_in_subreddit(user_data):
    post_author = user_data.post_author
    user_feed = (feedparser.parse("https://www.reddit.com" + post_author + ".rss"))['entries']
    for j in range(len(user_feed)):
        post_label = user_feed[j]['tags'][0]['term']
        for subreddit in SUBS_TO_CATCH:
            if subreddit == post_label:
                return True
    return False


# Initialize and run Discord bot
discordBot = DiscordBot()
discordBot.run(BOT_TOKEN)
