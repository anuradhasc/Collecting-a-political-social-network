
# coding: utf-8

# In[ ]:


"""
Created on Fri Sep  2 19:02:57 2016

@author: Anuradha Chaudhary
"""

# Imports you'll need.
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
import urllib.request
import requests

consumer_key = 'v6n6DjwGYKxYpKs2YqWu7AaZO'
consumer_secret = 'bliYNf7rbe0SylyPDexmTdOyQH5Aa3W4eWzinC7XG5y0AXiaDK'
access_token = '3430639648-o7RuG0zlsOsBGYs549sopsEwlpd84FiFUbTkHbh'
access_token_secret = 'QlG1pHVNxZZ1sxT3voTGvZ1Hf04I4IpuPNwOqJfJ2lg7s'


# This method is done for you. Make sure to put your credentials in the file twitter.cfg.
def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.
    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.
    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')
    ['DrJillStein', 'GovGaryJohnson', 'HillaryClinton', 'realDonaldTrump']
    """
    ###TODO
    #currURL = "https://github.com/iit-cs579/anuradhasc/blob/master/a0/candidates.txt"
    #response = urllib.request.urlopen(currURL)
    #lines = response.readlines()
    f = open(filename, "r")
    with open(filename) as f:
        candidateList = f.read().splitlines()
    f.close
    return candidateList
	
    


# I've provided the method below to handle Twitter's rate limiting.
# You should call this method whenever you need to access the Twitter API.
def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)
    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup
    In this example, I test retrieving two users: twitterapi and twitter.
    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """
    ###TODO
    r = robust_request(twitter,'users/lookup',{'screen_name' : ','.join(screen_names)})
    #print(r)
    users = []
    for x in r.get_iterator():
        users.append(x)
        """if 'name' in x:
            print(x['name'])"""
    return users


def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids
    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.
    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.
    Note: If a user follows more than 5000 accoun  ts, we will limit ourselves to
    the first 5000 accounts returned.
    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    #print("screen name get_friends",screen_name['screen_name'])
    r = robust_request(twitter,'friends/ids',{'screen_name':screen_name})   
    #print("Screen name ",screen_name['screen_name'])
    #print("Friends count ",screen_name['friends_count'])
    friends = []
    for x in r:
        friends.append(x)
    """print("Friends ",friends)"""
    return sorted(friends)
    

def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.
    Store the result in each user's dict using a new key called 'friends'.
    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing
    >>> twitter = get_twitter()
    >>> users = [{'screen_name': 'aronwc'}]
    >>> add_all_friends(twitter, users)
    >>> users[0]['friends'][:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    for u in users:
        u['friends'] = get_friends(twitter,u['screen_name'])
    """print(u['friends'])"""
    
def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    #print("Inside print num")
    for u in range(len(users)):
        print(users[u]['screen_name']+" "+str(users[u]['friends_count']))
    


def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter
    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    ###TODO
    counter = Counter()
    for i in range(len(users)):
        friend_ids = users[i]['friends']
        counter.update(friend_ids)
    """print(counter)"""
    return counter


def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.
    Args:
        users...The list of user dicts.
    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.
    In this example, users 'a' and 'c' follow the same 3 accounts:
    >>> friend_overlap([
    ...     {'screen_name': 'a', 'friends': ['1', '2', '3']},
    ...     {'screen_name': 'b', 'friends': ['2', '3', '4']},
    ...     {'screen_name': 'c', 'friends': ['1', '2', '3']},
    ...     ])
    [('a', 'c', 3), ('a', 'b', 2), ('b', 'c', 2)]
    """
    ###TODO
    friend_overlap = []
    #print("friend_overlap users ",users[0]['screen_name'])
    for i in range(len(users)):
        for j in (range(i+1,len(users))):
            c = Counter() 
            c.update(users[i]['friends'])
            c.update(users[j]['friends'])
            count = 0
            for x in c.keys():
                #print(c[x])
                if(c[x] > 1):
                    count += 1    
            if(users[i]['screen_name'] != users[j]['screen_name']):
                {
                friend_overlap.append((users[i]['screen_name'], users[j]['screen_name'], count))
                }
    friend_overlap = sorted(friend_overlap, key=lambda x:x[2], reverse = True)
    return friend_overlap
            


def followed_by_hillary_and_donald(users, twitter):
    """
    Find and return the screen_name of the one Twitter user followed by both Hillary
    Clinton and Donald Trump. You will need to use the TwitterAPI to convert
    the Twitter ID to a screen_name. See:
    https://dev.twitter.com/rest/reference/get/users/lookup
    Params:
        users.....The list of user dicts
        twitter...The Twitter API object
    Returns:
        A string containing the single Twitter screen_name of the user
        that is followed by both Hillary Clinton and Donald Trump.
    """
    ###TODO
    c = Counter()
    c.update(users[2]['friends'])
    c.update(users[3]['friends'])
    for x in c.keys():
        if c[x] > 1:
            """print(x);"""
            var_id = x;
            
    r = robust_request(twitter,'users/lookup',{'user_id' : var_id})
    for x in r.json():
        """print(x['screen_name'])"""
        follower = x['screen_name']
    return follower

def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)
        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.
    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """
    ###TODO
    G=nx.Graph()
    friends = []
    for x in range(len(users)):
        G.add_node(users[x]['screen_name'])
    #print(friend_counts)
    for x in friend_counts.keys():
        if friend_counts[x] > 1:
            friends.append(x)
            G.add_node(x)
    for i in range(len(users)):
        for x in friends:
            for u in users[i]['friends']:
                if(u == x):
                    {
                        #edge = (users[i]['screen_name'], u)
                        G.add_edge(users[i]['screen_name'], u)
                    }
    return G

def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).
    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.
    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    ###TODO
    fig = plt.figure(figsize=(22,22))
    labels = []
    listNodes = {}
    for u in range(len(users)):
        labels.append(users[u]['screen_name'])
    for node in graph.nodes():
        if node in labels:
            listNodes[node] = node 
    pos=nx.spring_layout(graph)
    nx.draw(graph,pos=pos, with_labels = False)
    nx.draw_networkx_labels(graph,pos, labels=listNodes, font_color='blue', font_weight='bold', alpha=1.5)
    plt.axis("off")
    plt.savefig(filename, format="PNG")
    plt.show()

def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))

    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



