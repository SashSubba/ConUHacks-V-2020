import os
import logging
from flask import Flask
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
import pandas as pd
from onboarding_tutorial import OnboardingTutorial

SLACK_API_TOKEN = "xoxb-923929175703-910617428419-LmY9FsB1LpV0wTj3g31tqMnX"
SLACK_SIGNING_SECRET = "e6a22c8e900ccc70f51f7f09fde585ae"

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Initialize a Web API client
slack_token = SLACK_API_TOKEN
slack_web_client = SlackClient(slack_token)

# Create simulation data.
df = pd.DataFrame({"DRIVER": ['Sonam', 'Sash', 'Matteo'],
                   "AVAILABILITY": ['7-9', '8-10', '6-8'],
                   "# SPOTS": [5, 4, 4]})

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})
    channel_id = event.get("channel")
    slack_web_client.api_call("chat.postMessage", channel=payload["event"]["channel"], text="Test output")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "test":
        slack_web_client.api_call("chat.postMessage", channel=payload["event"]["channel"], text="Test output")

    if text and text.lower() == "show table":
        slack_web_client.api_call("chat.postMessage", channel="general", text=df.to_csv(sep=' ', index=False, header=False))

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run(port=5000)