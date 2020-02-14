import praw
from os import getenv
from discord_webhook import DiscordWebhook
import time

class ProgrammingBuddiesBot:

    def __init__(self):
        self.last_id = None
        self.reddit = praw.Reddit(client_id=getenv('R_CLIENT_ID'), 
                                  client_secret=getenv("R_CLIENT_SECRET"), 
                                  user_agent='ProgrammingBuddiesBot')
        self.subreddit = getenv('SUBREDDIT')
        self.webhook_url = getenv("WEBHOOK")

    def loop(self):
        '''Request the newest Posts from a subreddit and post them to a
           Discord server Using webhook.
           Remembers ID of last post and will not post a submission twice.
           Will not post anything on the first run.'''
        sub = self.reddit.subreddit(self.subreddit)
        if self.last_id is None:
            posts = sub.new(limit=10)
            self.last_id = f't3_{list(posts)[0].id}'
            return
        else:
            # Convert ListingGenerator into List and then reverse
            posts = list(sub.new(limit=10, params={"before":self.last_id}))[::-1]

        for post in posts:
            self.hook(post.url)
            print(post.url)
            self.last_id = f't3_{post.id}'
    
    def hook(self, msg):
        webhook = DiscordWebhook(url=self.webhook_url, content=msg)
        response = webhook.execute()



if __name__ == "__main__":
    bot = ProgrammingBuddiesBot()
    print("running")
    while True:
        try:
            print("requesting")
            bot.loop()
            time.sleep(15*60)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(f'EXCEPTION\n{e}')


    

    