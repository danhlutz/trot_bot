I'm learning Python in my spare time and I started this project to help me get 
stronger -- and to show my love of the Old Man. 

## Release notes Nov. 1 2016

I have made a number of additions to the code to prepare to host it on Heroku. 

The biggest change is adding a .p 'pickle' data file to the repo to store the data the Bot uses to generate random tweets. 

## Acknowledgments
I modified the n-grams method in Joel Grus's _Data Science from Scratch_ to 
randomly generate the Trotsky quotes. Instead of trigrams, I used 4-grams, and
so actual quotes turn up more often. 

This bot crawls the magnificient collection of Trotsky's works at the 
Trotsky Internet Archive: https://www.marxists.org/archive/trotsky/works/index.htm. Many thanks to all the people and their hard work to make that such a 
great and comprehensive site. 

Finally, I got my inspiration from a novel of Ken MacLeod, where future members
of the Fourth International create an artificial intelligence based on 
Trotsky. We have a long way to go.

## Getting started

The current bot includes a pickled data file that the bot uses to generate random tweets. You can use that out of the box, or follow the instructions below to roll your own:

1. Create a Crawler, then run crawler.crawl() to scrape the TIA for links to content pages
2. Pickle the crawler using the .pickle_crawler method
3. Instantiate a bot and then run the accumulate_wisdom method to load pages from the TIA into the pages. 
4. use the send_tweet method to generate random tweets and send 'em
5. or use the send_tweet.py file to send a tweet from the CL or to schedule a tweet from a server 
