#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import json
import os
import sys
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

now = int(time.time())
CONFIG_FILE='config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
SLACK_USER_TOKEN = config['slack']['user_token']
SLACK_BOT_TOKEN = config['slack']['bot_token']
THRESHOLD = int(config['slack']['threshold'])
EXCLUDE_LIST = (config['slack']['exclude_list'])

DEBUG = False  # set True if test mode
if DEBUG:
    DEBUG_CHANNEL = (config['slack']['debug_channel'])


"""
###  get conversations info ###
#  conversations.list
#  ref: https://api.slack.com/methods/conversations.list
"""
client = WebClient(token=SLACK_USER_TOKEN)
convs = {}
try:
    response = client.conversations_list(exclude_archived=True)
    for channel in response['channels']:
        if not channel['name'] in EXCLUDE_LIST:
            convs[channel['id']] = channel['name']
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}", file=sys.stderr)


"""
###  get conversations last post ts ###
#  conversations.history
#  ref: https://api.slack.com/methods/conversations.history
"""
client = WebClient(token=SLACK_USER_TOKEN)
target_convs = {}
for id, name in convs.items():
    try:
        response = client.conversations_history(channel=id, limit=1)
        ts = int(float(response['messages'][0]['ts']))
        if THRESHOLD < now-ts:
            target_convs[id] = name
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}", file=sys.stderr)


"""
### Post remind message to channel
#  chat.postMessage
#  https://api.slack.com/methods/chat.postMessage
"""
client = WebClient(token=SLACK_BOT_TOKEN)
text = config['slack']['bot_message']
for id, name in target_convs.items():
    try:
        if DEBUG:
            id = DEBUG_CHANNEL
        response = client.chat_postMessage(channel=id, text=text)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}", file=sys.stderr)

