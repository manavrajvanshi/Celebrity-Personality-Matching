import sys
import requests
import json
import operator
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights 

pi_u = 'fc7bfa0c-7006-46c1-a271-cb108c536390'
pi_p = '8W535uTYmeK3'

user_handle = “#########”
celebrity_handle = “###########”

def analyze(handle):

    print "Processing,please wait..."


    twitter_consumer_key = ‘###########’
    twitter_consumer_secret = ‘###########’
    twitter_access_token = ‘##########’
    twitter_access_secret = ‘#########’

    twitter_api = twitter.Api(consumer_key=twitter_consumer_key,consumer_secret=twitter_consumer_secret,access_token_key=twitter_access_token,access_token_secret=twitter_access_secret)

    statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

    text = "" 
    for s in statuses:
        if (s.lang =='en'):
            text += s.text.encode('utf-8')

    pi_result = PersonalityInsights(username=pi_u, password=pi_p).profile(text)

    print ""
    return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data


def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
            compared_data[keys] = abs(dict1[keys] - dict2[keys])
    return compared_data


user_result = analyze(raw_input("Enter the user handle: "))
celebrity_result = analyze(raw_input("Enter the celebrity handle: "))

user = flatten(user_result)
celebrity = flatten(celebrity_result)


compared_results = compare(user,celebrity)


sorted_results = sorted(compared_results.items(), key=operator.itemgetter(1))


for keys, value in sorted_results[:]:
    res = keys+'\t\t'+str(user[keys])+'\t\t'+str(celebrity[keys])+'\t\t'+str(compared_results[keys])
    print res.rjust(75)
