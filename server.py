import praw
from os import getenv
from discord_webhook import DiscordWebhook
import time
import base36


class ProgrammingBuddiesBot:

    def __init__(self):
        self.reddit = praw.Reddit(client_id=getenv('R_CLIENT_ID'), 
                                  client_secret=getenv("R_CLIENT_SECRET"), 
                                  user_agent='ProgrammingBuddiesBot')
        self.subreddit = getenv('SUBREDDIT')
        self.webhook_url = getenv("WEBHOOK")
        self.last_id = -1
        self.fetch_size = int(getenv("FETCH_SIZE", 10))

    def loop(self):
        '''Request the newest Posts from a subreddit and post them to a
           Discord server Using webhook.
           Remembers ID of last post and will not post a submission twice.
           Will not post anything on the first run.'''

        sub = self.reddit.subreddit(self.subreddit)
        posts = list(sub.new(limit=self.fetch_size))[::-1]
        if self.last_id == -1:
            print("initial loop or unusable buffer yo")
            self.last_id = base36.loads(posts[-1].id)
            return

        for post in posts:
            if base36.loads(post.id) > self.last_id:
                self.hook(post.url)
                print(f't3_{post.id}: {post.url}')

        self.last_id = base36.loads(posts[-1].id)

    def hook(self, msg):
        webhook = DiscordWebhook(url=self.webhook_url, content=msg)
        webhook.execute()


if __name__ == "__main__":
    bot = ProgrammingBuddiesBot()
    waiting_time = int(getenv("WAITING_TIME", 15))
    print("running")
    while True:
        try:
            print("requesting")
            bot.loop()
            time.sleep(waiting_time * 60)
        except KeyboardInterrupt:
            exit()
        #except Exception as e:
        #    print(f'EXCEPTION\n{e}')
