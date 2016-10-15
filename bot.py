#trot_bot

import random, re
from collections import defaultdict

from bs4 import BeautifulSoup
import requests



class Bot:

    def __init__(self):
        # list of starter words
        self.start_words = []
        # dictionary of two word pairs, and the words that follow them,
        # stored as a list
        self.trigrams = defaultdict(list)

    def scrape_page(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')

        
        content = soup.find('div', 'article-body')
        regex = r"[\w']+|[\.]"
        
        # this overwrites whatever is already in wkg_docs
        # so you better do something about it earlier
        self.wkg_document = []

        for paragraph in soup('p'):
            words = re.findall(regex, fix_unicode(paragraph.text))
            self.wkg_document.extend(words)
# scrape a page and return a document 

# get a request from the Trotsky Internet Archive

# divide up the request into words

# zip(doc, doc[1:], doc[2:]
# add doc and doc[1:] to a dict, and append doc[2:]

# if doc == punctuation, add doc[1:] and doc[2:] to start words



# generate a random text string

# pick a start word at random

# keep going until you get a punctuation mark



# HELPER FUNCTIONS

def fix_unicode(text):
    return text.replace(u"\u2019", "'")







#LATER STUFF

# scrape the whole TIA
# first scrape for links. Build up a list of link

# pull a sample of k links, scrape all of them

# tweet


## TESTS
def test_bot_init():
    x = Bot()
    return type(x.start_words) == list and type(x.trigrams) == defaultdict


def test_fix_unicode():
    apos = u"'"
    apos2 = u"\u2019"
    return fix_unicode(apos) == "'" and fix_unicode(apos2) == "'"

def test_scrape():
    trotsky = Bot()
    url = "https://www.marxists.org/archive/trotsky/1940/07/letter04.htm"
    trotsky.scrape_page(url)
    return len(trotsky.wkg_document) > 0 



def test_func(func):
    print 'Testing: ', func.__name__, '\t','PASSED: ', func()
    if func():
        return 1
    else:
        return 0

def test():
    print '***************************************************'
    print 'BEGIN TESTING'
    print ''
    func_list = [
        test_bot_init,
        test_fix_unicode,
        test_scrape
        ]
    passed = sum([test_func(function) for function in func_list])
    total = len(func_list)
    print ''
    print 'PASSED: ', passed
    print 'FAILED: ', total - passed
    print '***************************************************'
        
    
