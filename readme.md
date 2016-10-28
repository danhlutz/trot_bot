I'm learning Python in my spare time and I started this project to help me get 
stronger -- and to show my love of the Old Man. 

## Acknowledgments
I modified the n-grams method in Joel Grus's Data Science from Scratch to 
randomly generate the Trotsky quotes. Instead of trigrams, I used 4-grams, and
so actual quotes turn up more often. 

This bot crawls the magnificient collection of Trotsky's works at the 
Trotsky Internet Archive: https://www.marxists.org/archive/trotsky/works/index.htm. Many thanks to all the people and their hard work to make that such a 
great and comprehensive site. 

Finally, I got my inspiration from a novel of Ken MacLeod, where future members
of the Fourth International create an artificial intelligence based on 
Trotsky. We have a long way to go.

## Getting started

I am going to add a setup function and function to tweet every hour. Until then here is how to set up a bot.
1. instantiate a Crawler, then run crawler.crawl() to scrape the TIA for links to content pages
2. pickle the crawler using the .pickle_crawler method
3. Instantiate a bot and then run the accumulate_wisdom method to load pages from the TIA into the pages. 
4. use the send_tweet method to generate random tweets and send 'em 
