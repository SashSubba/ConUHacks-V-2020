from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import os
import logging
from flask import Flask
import ssl as ssl_lib
import certifi
from onboarding_tutorial import OnboardingTutorial

# Our app's Slack Event Adapter for receiving actions via the Events API

SLACK_CLIENT_ID="910753403795.924432115862"
SLACK_CLIENT_SECRET= "485a4432f1679062fbf14735a43bc914"
SLACK_VERIFICATION_TOKEN="kwG3gH0rdCuQpzbdKsSAztTR"
SLACK_BOT_TOKEN="xoxb-910753403795-910754438179-QwKKpt6B4ctpxAXdtGF2RdF3"


slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Initialize a Web API client
slack_token = SLACK_API_TOKEN
slack_web_client = SlackClient(slack_token)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        slack_client.api_call("chat.postMessage", channel=channel, text=message)


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.api_call("chat.postMessage", channel=channel, text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)