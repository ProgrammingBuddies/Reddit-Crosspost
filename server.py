import praw
from os import getenv
from discord_webhook import DiscordWebhook
import time


class ProgrammingBuddiesBot:

    def __init__(self):
        self.reddit = praw.Reddit(client_id=getenv('R_CLIENT_ID'), 
                                  client_secret=getenv("R_CLIENT_SECRET"), 
                                  user_agent='ProgrammingBuddiesBot')
        self.subreddit = getenv('SUBREDDIT')
        self.webhook_url = getenv("WEBHOOK")
        self.buffer = []
        self.post_limit = int(getenv("POST_LIMIT", 10))
        self.buffer_size = int(getenv("BUFFER_SIZE", 100))

    def loop(self):
        '''Request the newest Posts from a subreddit and post them to a
           Discord server Using webhook.
           Remembers ID of last post and will not post a submission twice.
           Will not post anything on the first run.'''

        sub = self.reddit.subreddit(self.subreddit)
        for i, id in enumerate(self.buffer[::-1]):
            posts = list(sub.new(limit=self.post_limit, params={"before": id}))[::-1]
            if len(posts) > 0:
                self.buffer = self.buffer[:-1*i]
                break
        else:
            print("initial loop or unusable buffer yo")
            posts = sub.new(limit=10)
            self.buffer += [f't3_{post.id}' for post in list(posts)[::-1]]
            return

        for post in posts:
            self.hook(post.url)
            self.buffer.append(f't3_{post.id}')
            print(f't3_{post.id}: {post.url}')
    
    def clean(self):
        if len(self.buffer) > self.buffer_size:
            self.buffer = self.buffer[len(self.buffer) - self.buffer_size:]

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
        except Exception as e:
            print(f'EXCEPTION\n{e}')
