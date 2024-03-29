#!/usr/bin/env python
import yaml
import pathlib
import logging
import os
import argparse
import sys
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def resource(name):
    # Get a resource from either the same file as this script or the app bundle.
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys._MEIPASS) / name
    else:
        return pathlib.Path(__file__).parent / name


credentials = None
def obtain_credentials(credentials_file = resource("credentials.yaml")):
    with open(str(credentials_file)) as f:
        credentials = yaml.safe_load(f)
    return credentials

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

class SlackBotsChannelMessenger:

    def __init__(self, credentials):
        self._client = WebClient(token=credentials['bot_token'])
        self._bots_channel_id = None

    @property
    def bots_channel_id(self):
        if not self._bots_channel_id:
            LOG.info("Getting bots channel...")
            try:
                # Call the conversations.list method using the WebClient
                for result in self._client.conversations_list():
                    for channel in result["channels"]:
                        if channel['name'] == "bots":
                            # We found the bots channel
                            self._bots_channel_id = channel["id"]
                            LOG.info(f"Found channel id {self._bots_channel_id} for channel \"bots\"")
            except SlackApiError as e:
                ASSERT(False, e)
        return self._bots_channel_id

    def post_message(self, message, channel_id = None):
        if not channel_id: channel_id = self.bots_channel_id
        try:
            # Call the conversations.list method using the WebClient
            result = self._client.chat_postMessage(
                    channel=channel_id,
                    text=message
                    )
            LOG.info(f"Message post result: {result}")

        except SlackApiError as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    # When run not as a library, do our base logging config.
    import python_logging_base

    # Notice the handling of default arguments from a file...
    default_arguments_file = resource("defaults.yaml")
    with open(str(default_arguments_file)) as f:
        args = yaml.safe_load(f)
    parser = argparse.ArgumentParser(description="Send a Slack message.")
    parser.add_argument('--message', '-m', type=str, nargs='?')

    # Read default args from a file, and overwrite them with any called on the command line.
    # This is to populate a unified, expected set of args even if running from an app bundle, and to allow any
    # distributed app bundles to be modified at launch / changed default file values.
    parsed_args = parser.parse_args()
    args.update((k, v) for k,v in vars(parsed_args).items() if v is not None)

    # Set up the credentials
    c = obtain_credentials()
    messenger = SlackBotsChannelMessenger(c)
    message = args['message']
    LOG.info(f'Posting message "{message}"')
    messenger.post_message(args['message'])
