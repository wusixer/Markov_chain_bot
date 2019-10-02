import os
import slack
import json
import time
import glob
#  print(os.environ['SLACK_TOKEN'])
#  print(os.environ['SLACK_TOKEN'])
# autheticate as me with a token, we first initialize
#so that it can make requests to Slack’s Web API,
#in that way we don’t have to provide the token each time whencalling a method
client = slack.WebClient(token=os.environ['BOT_TOKEN'])

#returns a list of all channel-like conversations in a workspace.
#The "channels" returned depend on what the calling token has access to
list_response = client.conversations_list()
# make list of dicts to store the channel name and id
channels = [{'name': channel['name'], 'id': channel['id']} for channel in list_response['channels']]
#  print(channels)

#messages = []
word_from_individuals = {}
word_from_channels = {}
# get message from the user in each channel and
# append message one after another
# write out merged message to 1 file
for channel in channels:
    channel_id = channel['id']
    channel_value = channel['name']
    print("getting Everyone's messages from " + channel_value)
    history_response = client.channels_history(channel=channel_id, count=1000)
    # get words from a specfic person
    for message in history_response['messages']:
        if 'user' in message and 'text' in message:
            if message['user'] not in word_from_individuals:
                word_from_individuals[message['user']] = []
            print('getting words from'+ message['user'])
            word_from_individuals[message['user']].append(message['text'])

    # so we don't make too many request in a short amount of time
    time.sleep(1)
    # get words from a specfic channel
    for message in history_response['messages']:
        if 'text' in message:
            if channel['name'] not in word_from_channels:
                word_from_channels[channel['name']] = []
            if 'Hello' in message['text'] or 'Hi' in message['text']:
                continue
            print('getting words from'+ channel['name'])
            word_from_channels[channel['name']].append(message['text'])
    time.sleep(1)

with open('data/everyone_merged_file.json', 'w') as outfile:
    json.dump(word_from_individuals, outfile, sort_keys=True, indent=4)

with open('data/channel_merged_file.json', 'w') as outfile:
    json.dump(word_from_channels, outfile, sort_keys=True, indent=4)


