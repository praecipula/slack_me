#!/usr/bin/env python
import yaml
import pathlib
import logging
import os
import argparse
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

credentials = None
credentials_file = pathlib.Path(__file__).parent / "credentials.yaml"
with open(str(credentials_file)) as f:
    credentials = yaml.safe_load(f)

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=credentials['bot_token'])
LOG = logging.getLogger(__name__)

def get_bots_channel():
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
    return conversation_id

def post_message(message, channel_id = get_bots_channel()):
    try:
        # Call the conversations.list method using the WebClient
        result = client.chat_postMessage(
                channel=channel_id,
                text=message
                )
        LOG.info(f"Message post result: {result}")

    except SlackApiError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a Slack message.")
    parser.add_argument('--message', '-m', type=str, nargs='?', default="A message for you, sir. Not sure what it is, but *something* happened...")

    args = parser.parse_args()
    post_message(args.message)
