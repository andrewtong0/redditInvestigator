# redditInvestigator

### What it does and why
- In my spare time, I help moderate a few subreddits. Periodically, we would encounter waves of users from malicious subreddits that would attempt to flood our subreddits with inappropriate posts.
- This tool checks the most recent posters on a list of specified subreddits, and checks their account history. If they've participated in one of the user-defined malicious subreddits, the Discord bot will notify you of their post.

### Dependencies
- **feedparser**: Parses the Reddit RSS feed
- **discord.py**: To notify of malicious users
- **asyncio**: Allows for delay between subsequent checks

### Requirements
- **SUBS_TO_CHECK**: A list of subreddits to check the users from
- **SUBS_TO_CATCH**: A list of "malicious" subreddits to notify if a user has participated in them
- **CHECK_TIMER**: Time (in seconds) before another check is made for new users/posts
- **NUM_RECENT_USERS**: This number specifies how many of the most recent users it will check from each subreddit in SUBS_TO_CHECK
- **UUID_TO_PING**: (Optional) If desired, the bot will ping the UUID specified when a user is found
- **BOT_TOKEN**: Discord bot token to run script from

### How it works
- get_recent_users() gets the most recent posters from each subreddit in SUBS_TO_CHECK (gets NUM_RECENT_USERS from each) and creates a "UserData" object for each user, storing them in a list. The UserData object simply contains the post author, the link to their post, and their post title.
- user_in_subreddit() returns true if the post author from the UserData object has participated in one of the listed malicious subreddits.
- THe DiscordBot object initializes the background task (poll_check_users()) which continually runs get_recent_users() and user_in_subreddit(), and sends a message with the locally defined send_message() if a match is found.

### Important Notes and Planned Updates
- As it stands, the bot does not retain information on each call to poll_check_users(), meaning that if a malicious post is found and is not removed, it will continually detect (and notify you) of this post either until it is gone or it goes out of the NUM_RECENT_USERS scope. Planning on implementing database functionality that will be able to communicate and detect if a post has already been caught to prevent duplicate notifications.
- The bot only notifies you of the post, and does not yet remove the post itself. I am hoping to implement autoremoval with the Reddit API in the future.
