import markovify
#from custom_markov import markov
import os
import slack
import json
import re

DEBUG = True

# get the channels name and ID
#channel_sc = slack.WebClient(token=os.environ['SLACK_TOKEN'])
sc = slack.WebClient(token=os.environ['BOT_TOKEN'])
#list_response = channel_sc.conversations_list()
list_response = sc.conversations_list()
channels = {}

for channel in list_response['channels']:
    if channel['name'] not in channels:
        channels[channel['name']] = []
    channels[channel['name']] = channel['id']

# load the name_dict of users
name_dict = {
     'Tony': 'aaa',
    'Abbie': 'dcs',
    'Wennie': 'xyz',
    'Eric' : 'oxj',
    'Andy': 'fsd'
}

def get_user_id(user_name):
    """
    Get a user's displayed name using the slack id
    """
    return name_dict[user_name]

def _load_everyone_db():
    """
    Reads 'database' from a JSON file on disk.
    Returns a dictionary keyed by unique message permalinks.
    """

    with open('data/everyone_merged_file.json', 'r') as json_file:
        messages = json.loads(json_file.read())

    return messages

def _load_channel_db():
    """
    Reads 'database' from a JSON file on disk.
    Returns a dictionary keyed by unique message permalinks.
    """

    with open('data/channel_merged_file.json', 'r') as json_file:
        messages = json.loads(json_file.read())

    return messages

def _store_everyone_db(obj):
    """
    Takes a dictionary keyed by unique message permalinks and writes it to the JSON 'database' on
    disk.
    """

    with open('data/everyone_merged_file.json', 'w') as json_file:
        json_file.write(json.dumps(obj))

def _store_channel_db(obj):
    """
    Takes a dictionary keyed by unique message permalinks and writes it to the JSON 'database' on
    disk.
    """

    with open('data/channel_merged_file.json', 'w') as json_file:
        json_file.write(json.dumps(obj))

def build_text_model(trigger_id):
    """
    Read the latest 'database' off disk and build a new markov chain generator model.
    Returns TextModel.
    """
    if DEBUG:
        print("Building new model...")

    messages = _load_everyone_db()
    if trigger_id in name_dict.values():
        messages = messages[trigger_id]

    if trigger_id in list(channels.values()):
        messages = _load_channel_db()
        messages = messages[list(channels.keys())[list(channels.values()).index(trigger_id)]]

    if trigger_id == 'Company':
        messages = [item for sublist in list(messages.values()) for item in sublist]

    return markovify.Text(" ".join(messages), state_size=2)


def format_message(original):
    """
    Do any formatting necessary to markon chains before relaying to Slack.
    """
    if original is None:
        return '< No text is generated>'

    # Clear <> from urls
    cleaned_message = re.sub(r'<(htt.*)>', '\1', original)

    return cleaned_message



def main():
    """
    Startup logic and the main application loop to monitor Slack events.
    """

    # Create the slackclient instance
    # v2 version: https://github.com/slackapi/python-slackclient/wiki/Migrating-to-2.x
    sc = slack.RTMClient(token=os.environ['BOT_TOKEN'])
    # store incoming new messages either in JSON by user or JSON by channels
    @slack.RTMClient.run_on(event='message')
    def store_messages(**payload):
        data = payload['data']
        channel = data['channel']
        if 'user' in data and 'text' in data:
            msg = data['text']
            # don't store trigger word
            if 'Hello' not in msg and 'Hi' not in msg and data['user'] in name_dict.values():
                messages = _load_everyone_db()
                messages[data['user']].append(msg)
                _store_everyone_db(messages)
                if channel in list(channels.values()):
                    messages = _load_channel_db()
                    messages[list(channels.keys())[list(channels.values()).index(channel)]].append(msg)
                    _store_channel_db(messages)
                    print("added {} to corpus", msg)

    @slack.RTMClient.run_on(event='message')
    def say_Hello_name(**payload):
        data = payload['data']
        if 'text' not in data:
            return
        # make a list of trigger words
        trigger_everyone = ['Hello ' + i for i in list(name_dict.keys())]
        trigger_channel = ['Hello ' + i for i in list(channels.keys())]
        trigger_id = None

        if data['text'] in trigger_everyone:
            trigger_id = name_dict[data['text'][6:]]
        if data['text'] in trigger_channel:
            trigger_id = channels[data['text'][6:]]
        if data['text'] == "Hello Company":
            trigger_id = 'Company'

        if not trigger_id:
            return

        model = build_text_model(trigger_id)
        channel_id = data['channel']
        thread_ts = data['ts']

        webclient = payload['web_client']
        webclient.chat_postMessage(
            channel=channel_id,
            text="{}".format(format_message(model.make_sentence())),
            thread_ts=thread_ts,
            as_user = True

        )

    sc.start()

if __name__ == '__main__':
    main()

