import os
import json
import logging
from flask import Flask, request, make_response, Response
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
from carpool_request import carpoolRequest

SLACK_API_TOKEN = "xoxb-924426662630-922241501269-NKPAtLMsVFwRKB1SOTfwlgDA"
SLACK_SIGNING_SECRET = "14f9215c359a9134c404191ca9d4cb23"

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Initialize a Web API client
slack_token = SLACK_API_TOKEN
slack_web_client = SlackClient(slack_token)

carpool_request = carpoolRequest("general")

# Get the onboarding message payload
message = carpool_request.get_message_payload()

## Dictionary to store coffee orders. In the real world, you'd want an actual key-value store
COFFEE_ORDERS = {}

# Send a message to the user asking if they would like coffee
user_id = "UT62ALXQF"

order_dm = slack_web_client.api_call(
  "chat.postMessage",
  as_user=True,
  channel=user_id,
  text="I am Coffeebot, and I\'m here to help bring you fresh coffee :coffee:",
  attachments=[{
    "text": "",
    "callback_id": user_id + "coffee_order_form",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "actions": [{
      "name": "coffee_order",
      "text": ":coffee: Order Coffee",
      "type": "button",
      "value": "coffee_order"
    }]
  }]
)

COFFEE_ORDERS[user_id] = {
    "order_channel": order_dm["channel"],
    "message_ts": "",
    "order": {}
}

@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    message_action = json.loads(request.form["payload"])
    user_id = message_action["user"]["id"]

    if message_action["type"] == "interactive_message":
        # Add the message_ts to the user's order info
        COFFEE_ORDERS[user_id]["message_ts"] = message_action["message_ts"]

        # Show the ordering dialog to the user
        open_dialog = slack_web_client.api_call(
            "dialog.open",
            trigger_id=message_action["trigger_id"],
            dialog={
                "title": "Request a coffee",
                "submit_label": "Submit",
                "callback_id": user_id + "coffee_order_form",
                "elements": [
                    {
                        "label": "Coffee Type",
                        "type": "select",
                        "name": "meal_preferences",
                        "placeholder": "Select a drink",
                        "options": [
                            {
                                "label": "Cappuccino",
                                "value": "cappuccino"
                            },
                            {
                                "label": "Latte",
                                "value": "latte"
                            },
                            {
                                "label": "Pour Over",
                                "value": "pour_over"
                            },
                            {
                                "label": "Cold Brew",
                                "value": "cold_brew"
                            }
                        ]
                    }
                ]
            }
        )

        print(open_dialog)

        # Update the message to show that we're in the process of taking their order
        slack_web_client.api_call(
            "chat.update",
            channel=COFFEE_ORDERS[user_id]["order_channel"],
            ts=message_action["message_ts"],
            text=":pencil: Taking your order...",
            attachments=[]
        )

    elif message_action["type"] == "dialog_submission":
        coffee_order = COFFEE_ORDERS[user_id]

        # Update the message to show that we're in the process of taking their order
        slack_web_client.api_call(
            "chat.update",
            channel=COFFEE_ORDERS[user_id]["order_channel"],
            ts=coffee_order["message_ts"],
            text=":white_check_mark: Order received!",
            attachments=[]
        )

    return make_response("", 200)


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
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "daddy":
        slack_web_client.api_call("chat.postMessage", channel="general", text="GANG")



@slack_events_adapter.on("message")
def message2(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "request":
        slack_web_client.api_call("chat.postMessage", channel="general", text="GANG2")
        slack_web_client.chat_postMessage(channel="general",
                                          blocks=[
                                              {
                                                  "type": "modal",
                                                  "title": {
                                                      "type": "plain_text",
                                                      "text": "My App",
                                                      "emoji": True
                                                  },
                                                  "submit": {
                                                      "type": "plain_text",
                                                      "text": "Submit",
                                                      "emoji": True
                                                  },
                                                  "close": {
                                                      "type": "plain_text",
                                                      "text": "Cancel",
                                                      "emoji": True
                                                  },
                                                  "blocks": [
                                                      {
                                                          "type": "input",
                                                          "element": {
                                                              "type": "plain_text_input",
                                                              "action_id": "sl_input",
                                                              "placeholder": {
                                                                  "type": "plain_text",
                                                                  "text": "Placeholder text for single-line input"
                                                              }
                                                          },
                                                          "label": {
                                                              "type": "plain_text",
                                                              "text": "Label"
                                                          },
                                                          "hint": {
                                                              "type": "plain_text",
                                                              "text": "Hint text"
                                                          }
                                                      },
                                                      {
                                                          "type": "input",
                                                          "element": {
                                                              "type": "plain_text_input",
                                                              "action_id": "ml_input",
                                                              "multiline": True,
                                                              "placeholder": {
                                                                  "type": "plain_text",
                                                                  "text": "Placeholder text for multi-line input"
                                                              }
                                                          },
                                                          "label": {
                                                              "type": "plain_text",
                                                              "text": "Label"
                                                          },
                                                          "hint": {
                                                              "type": "plain_text",
                                                              "text": "Hint text"
                                                          }
                                                      }
                                                  ]
                                              }
                                          ]



                                          )


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run(port=3000)
