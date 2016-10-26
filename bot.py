#trot_bot
# but Mark should really up his game and learn git
# mark is really great

import random, re
from collections import defaultdict
import cPickle as pickle
from settings import *
from time import sleep
import string

from bs4 import BeautifulSoup
import requests



class Bot:

    def __init__(self):
        # list of starter words
        self.start_words = []
        # dictionary of two word pairs, and the words that follow them,
        # stored as a list
        self.trigrams = defaultdict(list)
        # a dict of short words to shorten tweets
        self.short_words = {
            'first': '1st',
            'second': '2nd',
            'third': '3rd',
            'fourth': '4th',
            'and': '&',
            'international': 'intl',
            'number': '#',
            'for': '4',
            'before': 'b4',
            'because': 'b/c',
            'forward': 'fwd',
            '#fourthinternational': random.choice(['#4thIntl', '#Intl4.0']),
            '#thirdinternational': random.choice(['#3rdIntl', '#Intl3.0']),
            '#secondinternational': '#2ndIntl',
            '#firstinternational': '#1stIntl',
            'lenin': random.choice(['#bigL', '#Lenin']),
            'marx': random.choice(['#bigM', '#Marx'])
            
            }
            

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
                result.append(current2)
                return result


    def hashtag_words(self, word_list, verbose=False):
        for i, word in enumerate(word_list):
            # check to see if the word and the next word start
            # with upper letters
            if i + 2 > len(word_list):
                break
            elif i != 0 and word[0] in string.uppercase and \
               word_list[i+1][0] in string.uppercase:
                hashtag = '#' + word + word_list[i+1]
                if verbose: print 'GOT ONE!: ', hashtag
                # if a double caps word pair is found, replace it in the string
                # and return it
                return word_list[:i] + [hashtag,] + word_list[i + 2:]
        # if we do not find a double-caps pair, look for the longest word
        # and hashtag it
        longest = 1
        # loop thru words and find the position of the longest.
        # sure there is a more pythonic way to do to this
        for i, word in enumerate(word_list):
            if len(word) >= len(word_list[longest]) and i != 0:
                longest = i
        # hashtag the word
        if verbose: print 'LONGEST:', longest
        hashtag = '#' + word_list[longest]
        if verbose: print 'GOT ONE!: ', hashtag
        return word_list[:longest] + [hashtag,] + word_list[longest + 1:] 
        # NEXT STEP: hashtag the longest word
        # ALSO --- needs test!
        return word_list

    def shorten_tweet(self, word_list, verbose=False):
        final_word_list = []
        # cycle thru words
        for word in word_list:
            # if word is int eh short words dict, append the dict value
            if word.lower() in self.short_words:
                if verbose: print 'Got one!: ', self.short_words[word.lower()]
                final_word_list.append(self.short_words[word.lower()])
            # else just append the word
            else:
                final_word_list.append(word)
        return final_word_list
        #NOW WRITE A TEST FOR THIS 
                
    def pickle_bot(self, filename='pickled_bot'):
        file_to_pickle = open(DATA_PATH + filename + '.p', 'wb')
        start_words_and_trigrams = (self.start_words, self.trigrams)
        pickle.dump(start_words_and_trigrams, file_to_pickle)
        file_to_pickle.close()


    def load_bot(self, filename='pickled_bot'):
        file_to_unpickle = open(DATA_PATH + filename + '.p', 'rb')
        self.start_words, self.trigrams = pickle.load(file_to_unpickle)
        file_to_unpickle.close()


    def accumulate_wisdom(self, num_pages=20, verbose=False):
        # init and load a crawler. Crawler must have already scraped
        # content pages
        crawler = Crawler()
        crawler.load_crawler()
        # return a list of pages to crawl
        pages_to_crawl = random.sample(crawler.content, num_pages)
        # for each page, scrape it, then add it to the trigrams
        for page in pages_to_crawl:
            sleep(30)
            if verbose: print 'Scraping: ', page
            self.scrape_page(page)
            self.add_fourgrams()
            if verbose: print 'Start words: ', len(self.start_words), \
               'nGrams: ', len(self.trigrams)               
            
        print 'Accumulated the historical wisdom of ' + str(num_pages) + \
              ' works of the old man.'



    ## ADD FUNCTION TO TURN WORD LIST INTO SENTENCE            
##                final = " ".join(result)
##                return final[:-2] + current2

    
    
            

    # add tweetify functions

    # add hashtagger

    # add word shortener


    # and tweet generator. Steps:
    # generate random word
    # hashtag it
    # shorten words
    # if < 160 characters, return it 


class Crawler():

    def __init__(self, seed='https://www.marxists.org/archive/trotsky/works/index.htm'):
        self.content = set()
        self.indexes = {}
        self.add_index(seed)

    def add_index(self, url):
        if url in self.indexes:
            pass
        else:
            self.indexes[url] = False


    def scrape_page(self, mother_url, verbose=False):
        html = requests.get(mother_url).text
        soup = BeautifulSoup(html, 'html5lib')
        for link in soup.find_all('a'):
            daughter_url = link.get('href')
            if verbose: print daughter_url
            if daughter_url == None: continue
            if classify_link(daughter_url) == 'content':
                full_link = combine_links(mother_url, daughter_url)
                self.content.add(full_link)
            elif classify_link(daughter_url) == 'index':
                full_link = combine_links(mother_url, daughter_url)
                if full_link == 'https://www.marxists.org/archive/trotsky/index.htm':
                    continue
                self.add_index(full_link)

    def pickle_crawler(self, filename='pickle_crawler'):
        file_to_pickle = open(DATA_PATH + filename + '.p', 'wb')
        index_and_content = (self.indexes, self.content)
        pickle.dump(index_and_content, file_to_pickle)
        file_to_pickle.close()


    def load_crawler(self, filename='pickle_crawler'):
        file_to_unpickle = open(DATA_PATH + filename + '.p', 'rb')
        self.indexes, self.content = pickle.load(file_to_unpickle)
        file_to_unpickle.close()


    def find_unscraped_link(self):
        for key, value in self.indexes.items():
            if value == False:
                return key
        return None

    def crawl(self):
        n = 0
        while sum([value for value in self.indexes.values()]) < \
              len(self.indexes):
            n += 1
            link_to_crawl = self.find_unscraped_link()
            self.indexes[link_to_crawl] = True
            self.scrape_page(link_to_crawl)
            print 'Crawled: ', link_to_crawl
            print 'Indexes: ', len(self.indexes), \
                  'Content: ', len(self.content)
            print 'Indexes crawled: ', n
            sleep(10)
        self.pickle_crawler()
            
        
        
    

    

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


def find_next_to_last_slash(url):
    slash = 0
    for i, char in enumerate(url):
        if char == '/':
            next_to_last = slash
            slash = i
    return next_to_last


def find_last_slash(url):
    for i, char in enumerate(url):
        if char == '/':
            slash = i
    return slash


def combine_links(mother, daughter):
    if daughter[:2] == '..':
        return mother[:find_next_to_last_slash(mother)] + daughter[2:]
    return mother[:find_last_slash(mother) + 1] + daughter



    









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


def test_combine():
    return combine_links('http://cnn.com/stuff/here.htm', 'friends.htm') == \
           'http://cnn.com/stuff/friends.htm' and \
           combine_links('http://example.com/mystuff/archives/index.htm', \
                         '../friendex.htm') == \
                         'http://example.com/mystuff/friendex.htm'


def test_add_index():
    y = Crawler()
    y.add_index('stuff')
    y.add_index('fruit')
    y.add_index('apples')
    y.indexes['stuff'] = True
    y.add_index('stuff')
    y.add_index('apples')
    return y.indexes['stuff'] == True and \
           y.indexes['fruit'] == False and \
           y.indexes['apples'] == False


def test_crawler_scrape():
    y = Crawler()
    y.scrape_page('https://www.marxists.org/archive/trotsky/britain/index.htm')
    return len(y.content) == 9

def test_find_unscraped_link():
    y = Crawler()
    y.scrape_page('https://www.marxists.org/archive/trotsky/britain/index.htm')
    return y.find_unscraped_link() != None


def hashtag_tests(verbose=False):
    x = Bot()
    double_cap = ['Should', 'trigger', 'a', 'Double', 'Cap']
    double_cap2 = ['Should', 'Trigger', 'A', 'double', 'cap']
    long_word = ['How', 'looooooooooooooooooooong', 'does', 'this', 'need']
    long_word_end = ['long', 'word', 'ennnnnnnnnnnnnnnnnnnnnnnnd']
    two_longs = ['Two', 'looong', 'shoort']
    last_cap = ['Only', 'the', 'last', 'is', 'CAP']
    to_test = [
        double_cap,
        double_cap2,
        long_word,
        long_word_end,
        two_longs,
        last_cap
        ]
    results = [x.hashtag_words(test_list, verbose=verbose)
               for test_list in to_test]
    return results[0][3] == '#DoubleCap' and \
           results[1][1] == '#TriggerA' and \
           results[2][1] == '#looooooooooooooooooooong' and \
           results[3][2] == '#ennnnnnnnnnnnnnnnnnnnnnnnd' and \
           results[4][2] == '#shoort'

def test_shorten_tweet(verbose=False):
    x = Bot()
    words = ['This', 'is', 'the', 'Fourth', 'International']
    words2 = ['And', 'this', 'is', 'for', 'my', 'first', 'friend', 'LENIN']
    words3 = ['For', 'you', 'and', 'the', 'FIRST', 'International']
    words4 = ['Any', 'tags', 'here']
    to_test = [words, words2, words3, words4]
    results = [x.shorten_tweet(x.hashtag_words(word_list), verbose)
               for word_list in to_test]
    return results[1][3] == '4' and \
           results[2][0] == '4' and \
           results[2][2] == '&'

def test_pickler(verbose=False):
    x = Bot()
    x.scrape_page('https://www.marxists.org/archive/trotsky/1924/ffyci-1/ch02.htm')
    x.add_fourgrams()
    xstart_words1 = len(x.start_words)
    xtrigrams1 = len(x.trigrams)
    x.scrape_page('https://www.marxists.org/archive/trotsky/1909/xx/tia09.htm')
    x.add_fourgrams()
    xstart_words2 = len(x.start_words)
    xtrigrams2 = len(x.trigrams)
    x.pickle_bot(filename='test_bot')
    y = Bot()
    y.load_bot(filename='test_bot')
    ystart_words = len(y.start_words)
    ytrigrams = len(y.trigrams)
    if verbose:
        print 'X Round 1 start_words: ', xstart_words1, ' trigrams: ', xtrigrams1
        print 'X Round 2 start_words: ', xstart_words2, ' trigrams: ', xtrigrams2
        print 'Y Round 1 start_words: ', ystart_words, ' trigrams: ', ytrigrams
    return xstart_words1 < xstart_words2 and \
           xtrigrams1 < xtrigrams2 and \
           xtrigrams2 == ytrigrams and \
           xstart_words2 == ystart_words
        

    

# testing harness
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
    # list of tests to be run
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
        test_find_last_slash,
        test_combine,
        test_add_index,
        test_crawler_scrape,
        test_find_unscraped_link,
        hashtag_tests,
        test_shorten_tweet,
        test_pickler
        ]
    # will print individual test results before summing results
    passed = sum([test_func(function) for function in func_list])
    total = len(func_list)
    print ''
    print 'PASSED: ', passed
    print 'FAILED: ', total - passed
    print '***************************************************'
        
    
