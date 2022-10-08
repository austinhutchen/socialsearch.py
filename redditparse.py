import pandas as pd
import requests
from operator import itemgetter
import time

data_type = "comment"     # give me comments, use "submission" to publish something
# Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
duration = "30d"
size = 1000               # maximum 1000 comments
# Sort by score (Accepted: "score", "num_comments", "created_utc")
sort_type = "score"
sort = "desc"             # sort descending
aggs = "subreddit"


def get_pushshift_data(data_type, **kwargs):
    """
    Gets data from the pushshift api.

    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.

    Read more: https://github.com/pushshift/api
    """

    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
    payload = kwargs
    try:
        data = requests.get(base_url, params=payload)
        return data.json()
    except:
        print('Search failed.')
        quit()


def get_reddit(ans, listing, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{ans}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()


def get_post_titles(r):
    '''
    Get a List of post titles
    '''
    posts = []
    for post in r['data']['children']:
        x = post['data']['title']
        posts.append(x)
    return posts


def get_results(r):
    '''
    Create a DataFrame Showing Title, URL, Score and Number of Comments.
    '''
    myDict = {}
    try:
        for post in r['data']['children']:
            myDict[post['data']['title']] = {
                'score': post['data']['score'], 'comments': post['data']['num_comments']}
        df = pd.DataFrame.from_dict(myDict, orient='index')
        return df
    except:
        print('An error occured.')


if __name__ == '__main__':
    limit = 50
    timeframe = 'week'  # hour, day, week, month, year, all
    listing = 'hot'  # controversial, best, hot, new, random, rising, top
    print('---REDDIT SEARCH V.1---')
    print('1 -> Search keyword')
    print('2 -> View subreddit')
    print('3 -> Show random post')
    main_choice = int(input('Choose an option: '))
    if main_choice == 1:
        while exit != 1:
            ans = input('Enter the keyword you want more information on: ')
            if ans.lower() == 'end':
                quit()
            else:
                print('ENTER 1 FOR MOST COMMON COMMENTS')
                print('ENTER 2 FOR MOST COMMON SUBREDDITS')
                print('ENTER 3 FOR MOST COMMON USERS')
                choice = int(
                    input('Would you prefer comments, users, or subreddits?: '))
                if choice == 1:
                    t1 = time.time()
                    data = get_pushshift_data(
                        data_type=data_type, q=ans, after=duration, size=size, aggs=aggs)
                    df = pd.DataFrame.from_records(data)[0:1000]
                    for i in range(0, 11):
                        # edit here for comment body
                        print(df.loc[i]['data']['body'])
                        print('')
                        print(df.loc[i]['data']['permalink'])
                        print('----end----')
                    t2 = time.time()
                    print(t2-t1, 'seconds taken to search comments.')
                # build subreddit searcher here
                elif choice == 2:
                    t1 = time.time()
                    data = get_pushshift_data(
                        data_type=data_type, q=ans, after=duration, size=size, aggs=aggs)
                    df = pd.DataFrame.from_records(data)[0:100]
                    for i in range(0, 11):
                        # edit here for comment body
                        print(df.loc[i]['data']['subreddit'])
                        print('----end----')
                    t2 = time.time()
                    print(t2-t1, 'seconds taken to search subreddits.')
                elif choice == 3:
                    t1 = time.time()
                    data = get_pushshift_data(
                        data_type=data_type, q=ans, after=duration, size=size, aggs=aggs)
                    df = pd.DataFrame.from_records(data)[0:100]
                    for i in range(0, 11):
                        # edit here for comment body
                        print(df.loc[i]['data']['author'])
                        print('----end----')
                    t2 = time.time()
                    print(t2-t1, 'seconds taken to search users.')

    if main_choice == 2:
        choice = input('Enter the subreddit you would like to search for: ')
        t1 = time.time()
        r = get_reddit(choice, listing, limit, timeframe)
        df = get_results(r)
        print(df[0]['data'])
        for i in range(0, 11):
            print(df.loc[i]['data']['author'])
            print('----end----')
        t2 = time.time()
        print(t2-t1, 'seconds taken to search users.')

    if main_choice == 3:

        post = 0
        print('Your random post of the day is: {}'.format(post))
    else:
        quit()
