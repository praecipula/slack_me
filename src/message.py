#!/usr/bin/env python
import yaml
import pathlib
import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

credentials = None
credentials_file = pathlib.Path(__file__).parent / "credentials.yaml"
with open(str(credentials_file)) as f:
    credentials = yaml.safe_load(f)

print(credentials)


# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=credentials['bot_token'])
LOG = logging.getLogger(__name__)
conversation_id = None
try:
    # Call the conversations.list method using the WebClient
    for result in client.conversations_list():
        for channel in result["channels"]:
            if channel['name'] == "bots":
                conversation_id = channel["id"]
                LOG.info(f"Found channel id {conversation_id} for channel \"bots\"")
            print(f"Found conversation: {channel['name']} : {conversation_id}")
except SlackApiError as e:
    print(f"Error: {e}")


message = "It's time to check something you were working on"
try:
    # Call the conversations.list method using the WebClient
    result = client.chat_postMessage(
            channel=conversation_id,
            text=message
            )
    LOG.info(f"Message post result: {result}")

except SlackApiError as e:
        print(f"Error: {e}")
