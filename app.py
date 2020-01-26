import os
import logging
from flask import Flask
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
from onboarding_tutorial import OnboardingTutorial

SLACK_BOT_TOKEN = 'xoxb-910753403795-910754438179-QwKKpt6B4ctpxAXdtGF2RdF3'
SLACK_SIGNING_SECRET = 'fefff8b45cd857d666eb94bc9b725e05'

slack_token = SLACK_BOT_TOKEN
slack_web_client = SlackClient(slack_token)

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        slack_web_client.api_call("chat.postMessage", channel="general", text="message")


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    SlackClient.api_call("chat.postMessage", channel=channel, text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
if __name__ == "__main__":
    app.run(port=3000)
