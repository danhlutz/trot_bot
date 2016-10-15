#trot_bot

from collections import defaultdict



class Bot:

    def __init__(self):
        self.start_words = []
        self.trigrams = defaultdict(list)

# scrape a page

# get a request from the Trotsky Internet Archive

# divide up the request into words

# zip(doc, doc[1:], doc[2:]
# add doc and doc[1:] to a dict, and append doc[2:]

# if doc == punctuation, add doc[1:] and doc[2:] to start words



# generate a random text string

# pick a start word at random

# keep going until you get a punctuation mark









#LATER STUFF

# scrape the whole TIA
# first scrape for links. Build up a list of link

# pull a sample of k links, scrape all of them

# tweet


## TESTS
def test_bot_init():
    x = Bot()
    return type(x.start_words) == list and type(x.trigrams) == defaultdict



def test_func(func):
    print 'Testing: ', func.__name__, 'PASSED: ', func()
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
        ]
    passed = sum([test_func(function) for function in func_list])
    total = len(func_list)
    print ''
    print 'PASSED: ', passed
    print 'FAILED: ', total - passed

        
    
