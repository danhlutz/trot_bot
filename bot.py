#trot_bot
# but Mark should really up his game and learn git
# mark is really great

import random, re
from collections import defaultdict
import cPickle as pickle
from settings import *

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
        # scrape single url and return a list of words
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
 
##    def add_trigrams(self):
##        new_trigrams = zip(self.wkg_document, \
##                       self.wkg_document[1:], \
##                       self.wkg_document[2:])
##        for prev, current, next in new_trigrams:
##            if prev == '.':
##                (self.start_words).append(current)
##            self.trigrams[(prev, current)].append(next)
##
    def add_fourgrams(self, verbose=False):
        new_fourgrams = zip(self.wkg_document, \
                       self.wkg_document[1:], \
                       self.wkg_document[2:], \
                       self.wkg_document[3:])
        for prev, current1, current2, next_word in new_fourgrams:
            if prev == '.':
                (self.start_words).append((current1, current2))
            if current2 == '2015' and verbose: print next_word
            self.trigrams[(prev, current1, current2)].append(next_word)
##        for key, value in self.trigrams.items():
##            if len(value) == 0:
##                if verbose: print 'Deleting: ', key, value
##                del self.trigrams[key]

##    def generate_words(self):
##        current = random.choice(self.start_words)
##        prev = '.'
##        result = [current]
##        while True:
##            next_word = random.choice(self.trigrams[(prev, current)])
##            prev, current = current, next_word
##            result.append(current)
##            if current in ['.', '?', '!']:
##                final = " ".join(result)
##                return final[:-2] + current

    def generate_words_fourgrams(self, verbose=False):
        current1, current2 = random.choice(self.start_words)
        prev = '.'
        result = [current1, current2]
        while True:
            next_word_list = self.trigrams[(prev, current1, current2)]
            if next_word_list == []:
                if verbose:
                    print '***********************'
                    print 'GOT ONE: ', prev, current1, \
                   current2
                    print '***********************'
                current1, current2 = random.choice(self.start_words)
                prev = '.'
                result = [current1, current2]
                continue

            next_word = random.choice(next_word_list)
            prev, current1, current2 = current1, current2, next_word
            result.append(current2)
            if current2 in ['.', '?', '!']:
                final = " ".join(result)
                return final[:-2] + current2
    
            

    # add tweetify functions

    # add hashtagger

    # add word shortener


    # and tweet generator. Steps:
    # generate random word
    # hashtag it
    # shorten words
    # if < 160 characters, return it 


def Crawler():

    def __init__(self):
        self.to_get_links = {}
        self.to_scrape = {}


    # helper functions needed
    # return true or false if it is a page in the TIA
    # return true or false if it is an index page -- need to get links
    # return true or fale if it is a page to be scraped
        


# HELPER FUNCTIONS

def fix_unicode(text):
    return text.replace(u"\u2019", "'")


def is_archive(url):
    # first three letters are two dots and a slash
    return (url[-3:] == 'htm' or url[-4:] == 'html') and \
           ((url[:3] == '../' and url[3:5] != '..') or \
            (url[:1] != '.'))


def classify_link(url):
    if is_archive(url) == False:
        return None
    if url[-9:] == 'index.htm' or url[-10:] == 'index.html':
        return 'index'
    else:
        return 'content'


def find_last_slash(url):
    for i, char in enumerate(url):
        if char == '/':
            slash = i
    return slash


def pickle_bot(bot, filename='save_bot'):
    file_to_pickle = open(DATA_PATH + filename + '.p', 'wb')
    
    pickle.dump(bot, file_to_pickle)
    file_to_pickle.close()
    









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

def test_add_trigrams():
    trotsky = Bot()
    url = 'https://www.marxists.org/archive/trotsky/1940/08/hitsarmies.htm'
    trotsky.scrape_page(url)
    trotsky.add_trigrams()
    
    return trotsky.start_words[0] == u'First'
    
def test_add_trigrams2():
    trotsky = Bot()
    url = 'https://www.marxists.org/archive/trotsky/1940/08/hitsarmies.htm'
    trotsky.scrape_page(url)
    trotsky.add_trigrams()
    len1 = len(trotsky.start_words)
    url = 'https://www.marxists.org/archive/trotsky/1940/08/letter11.htm'
    trotsky.scrape_page(url)
    trotsky.add_trigrams()
    
    return len(trotsky.start_words) > len1

def test_generate_words():
    trotsky = Bot()
    url = 'https://www.marxists.org/archive/trotsky/1940/08/hitsarmies.htm'
    trotsky.scrape_page(url)
    trotsky.add_trigrams()
    
    return len(trotsky.generate_words()) > 0
    
def test_generate_fourgrams():
    trotsky = Bot()
    url = 'https://www.marxists.org/archive/trotsky/1940/08/hitsarmies.htm'
    trotsky.scrape_page(url)
    trotsky.add_fourgrams()
    
    return len(trotsky.generate_words_fourgrams()) > 0 and \
           len(trotsky.start_words[0]) == 2

def test_generate_lots_of_fourgrams():
    trotsky = Bot()
    url = 'https://www.marxists.org/archive/trotsky/1940/08/hitsarmies.htm'
    trotsky.scrape_page(url)
    trotsky.add_fourgrams()

    n = 0

    for i in range(100):
        try:
            trotsky.generate_words_fourgrams()
            n += 1
        except IndexError:
            continue
    return n == 100


def test_generate_lots_of_fourgrams2():
    trotsky = Bot()
    url = 'https://www.marxists.org/archive/trotsky/1924/lit_revo/ch05.htm'
    trotsky.scrape_page(url)
    trotsky.add_fourgrams()

    n = 0

    for i in range(100):
        try:
            trotsky.generate_words_fourgrams()
            n += 1
        except IndexError:
            continue
    return n == 100
           

def test_keys():
    trotsky = Bot()
    url = 'https://www.marxists.org/archive/trotsky/1940/08/hitsarmies.htm'
    trotsky.scrape_page(url)
    trotsky.add_fourgrams()
    n = 0

    for key in trotsky.trigrams.keys():
        if len(key) == 3: n+= 1
    return n == len(trotsky.trigrams.items())

def test_is_archive():
    archives = ['../1924/ffyci-1/app02.htm',
                '../1924/ffyci-1/app03.htm',
                '../1924/ffyci-1/app04.htm',
                '../1924/ffyci-1/ch01.htm',
                'rp03.htm',
                'rp-intro.htm'
                ]
    not_archives = ['../military-pdf/Military-Writings-Trotsky-v1.pdf',
                    '#a1922',
                    '#a1923',
                    '#a1924',
                    '../../../../admin/legal/cc/by-sa.htm'
                    ]
    return sum([is_archive(link) for link in archives]) == len(archives) and \
           sum([is_archive(link) for link in not_archives]) == 0
           


def test_classify():
    contents = ['../1940/xx/party.htm', 
                '../1940/08/last-article.htm',
                '../1940/xx/jewish.htm',
                '../1940/05/stalin.htm'
                ]
    indexes = ['../china/index.htm',
               '../britain/index.htm',
               '../germany/index.htm',
               '../spain/index.htm'
               ]
    not_stuff = ['../../../xlang/trotsky.htm',
                 '../../../admin/volunteers/biographies/dwalters.htm',
                 '#a1934'
                 ]
    return sum([classify_link(link) == 'content' for link in contents]) \
           == len(contents) \
           and sum([classify_link(link) == 'index' for link in indexes]) \
           == len(indexes) \
           and sum([classify_link(link) == None for link in not_stuff]) \
           == len(not_stuff)

def test_find_last_slash():
    return find_last_slash('/') == 0 and \
           find_last_slash('../') == 2 and \
           find_last_slash('../../') == 5


    
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
        test_scrape,
        #test_add_trigrams,
        #test_add_trigrams2,
        #test_generate_words,
        test_generate_fourgrams,
        test_keys,
        test_generate_lots_of_fourgrams,
        test_generate_lots_of_fourgrams2,
        test_is_archive,
        test_classify,
        test_find_last_slash
        ]
    passed = sum([test_func(function) for function in func_list])
    total = len(func_list)
    print ''
    print 'PASSED: ', passed
    print 'FAILED: ', total - passed
    print '***************************************************'
        
    
