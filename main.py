import operator
import requests
import json
from apiclient.discovery import build

API_KEY = 'YOUR_API_KEY'
youtube = build('youtube','v3',developerKey = API_KEY)

#prompts user for the query and then calls the API
keyWord = input('Enter your search query:  ')
request = youtube.search().list(q=keyWord, part='snippet',type='channel', maxResults=20)
res = request.execute()

#parses through the json and saves each channel in a list
channels = []
for channel in res['items']:
    request = youtube.channels().list(part="snippet, statistics", id= channel['id']['channelId'])
    response = request.execute()
    channels.append({'name': response['items'][0]['snippet']['title'],
                     'subs': int(response['items'][0]['statistics']['subscriberCount']),
                     'description': response['items'][0]['snippet']['description']})

#sorts the channel list by the number of subscribers, from greatest to least
output = sorted(channels, key = operator.itemgetter('subs'), reverse=True)


#rudimentary formatting for output
print("Channels related to: " + keyWord + "\n")
print("Channel Name             |        Subscribers        |        Languages\n")

for c in output:
    d = c['description']
    langs = []
    if "Python" in d or "python" in d:
        langs.append("Python")
    if "Flutter" in d or "flutter" in d:
        langs.append("Flutter/Dart")
    if "React" in d or "react" in d:
        langs.append("React")
    if "Java" in d or "java" in d:
        langs.append("Java")
    if "Swift" in d or "swit" in d:
        langs.append("Swift")
    if c['subs'] >= 10000:
        print(c['name'][:25], end="")
        for i in range(28-len(c['name'][:25])):
            print("", end = " ")
        print(c['subs'], end="")
        for i in range(28-len(str(c['subs']))):
            print("", end = " ")
        for l in langs:
            print(l, end=", ")
        print()
