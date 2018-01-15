import csv
import json
import time
import tweepy


# You must use Python 2.7.x
# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>
    data_file = open(key_file, 'r')
    data = json.load(data_file)
    # Load keys here and replace the empty strings in the return statement with those keys
    data_file.close()
    return data["api_key"], data["api_secret"], data["token"], data["token_secret"]


# Q1.b.(i) - 5 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    count = 0
    for friend in tweepy.Cursor(api.friends, screen_name=root_user).items():
        primary_friends.append((root_user, friend.screen_name))
        count += 1
        if (count == no_of_friends):
            break

    # Add code here to populate primary_friends
    return primary_friends


# Q1.b.(ii) - 7 points
def getNextLevelFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    next_level_friends = []
    for cur_friend in friends_list:
        count = 0
        for friend in tweepy.Cursor(api.friends, screen_name=cur_friend).items():
            next_level_friends.append((cur_friend, friend.screen_name))
            count += 1
            if (count == no_of_friends):
                break
        time.sleep(60)

    # Add code here to populate next_level_friends
    return next_level_friends


# Q1.b.(iii) - 7 points
def getNextLevelFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])
    next_level_followers = []
    for cur_follower in followers_list:
        count = 0
        for follower in tweepy.Cursor(api.followers, screen_name=cur_follower).items():
            next_level_followers.append((follower.screen_name, cur_follower))
            count += 1
            if (count == no_of_followers):
                break
        time.sleep(60)

    # Add code here to populate next_level_followers
    return next_level_followers


# Q1.b.(i),(ii),(iii) - 4 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends.

    all_edges = []
    primary_friends = getPrimaryFriends(api, root_user, no_of_neighbours)
    friends_list = []
    for friend in primary_friends:
        friends_list.append(friend[1])
    time.sleep(60)
    next_level_friends = getNextLevelFriends(api, friends_list, no_of_neighbours)
    next_level_followers = getNextLevelFollowers(api, friends_list, no_of_neighbours)
    all_edges = primary_friends + next_level_friends + next_level_followers
    # Add code here to populate all_edges
    return all_edges


# Q1.b.(i),(ii),(iii) - 5 Marks
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    csvfile = open(output_file, 'w')
    fieldnames = ['Source', 'Target']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for each in data:
        writer.writerow({'Source': each[0], 'Target': each[1]})
    csvfile.close()
    pass


"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""


def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)
    
    writeToFile(edges, OUTPUT_FILE_GRAPH)



if __name__ == '__main__':
    testSubmission()
