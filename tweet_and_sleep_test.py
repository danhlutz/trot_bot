from bot import *



x = Bot()
x.load_bot()

for _ in range(10):
    x.send_tweet()
    sleep(30)
