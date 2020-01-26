import os
import logging
from flask import Flask
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
import pandas as pd
from tabulate import tabulate

# Bot parameters
SLACK_API_TOKEN = "xoxb-923929175703-910617428419-LmY9FsB1LpV0wTj3g31tqMnX"
SLACK_SIGNING_SECRET = "e6a22c8e900ccc70f51f7f09fde585ae"

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Initialize a Web API client
slack_token = SLACK_API_TOKEN
slack_web_client = SlackClient(slack_token)

def generate_lift_recommendation(locations):
    """
    Steps:
        1. Convert postal codes to longitude and latitude
        2. Find the distance between points in (1.)
        3. Find the closest match in the list of potential drivers (driver home vs. passenger home addresses)

    Args:
        locations (list) -- list of cities of drivers and passengers for comparison

    Returns:
        String -- Combination of pass and dri that should go together.
    """
    for i in len(pairs_of_locations):
        loc_a = (41.49008, -71.312796)
        loc_b = (42.499498, -81.695391)
        loc_c = (41.49008, -71.312796)
        loc_d = (41.799498, -80.695391)
    print(great_circle(newport_ri, cleveland_oh).kilometers)
    return 1


# Create simulation data.
df = pd.DataFrame({"Name": ['Sonam', 'Sash', 'Matteo'],
                   "Driver": ['N', 'Y', 'Y'],
                   "Hours": ['7-9', '8-10', '6-8'],
                   "City": ["St-Leonard", "Chomedey", "Anjou"],
                   "Long": [45.5875, 45.5384, 45.6160],
                   "Lat": [-73.5970, -73.7362, -73.5694]})

# To modify once we know the actual workspace IDs
# distance = {"USSJ5CLCB": "Mark"}

# Message events.
@slack_events_adapter.on("message")
def message(payload):
    """Process user requests here.
    """
    df_new = df.copy()
    event = payload.get("event", {})
    user_id = event.get("user")
    name = "Mark"
    text = event.get("text")

    # Hardcode the channel_id to be the carpooling channel
    # channel_id = event.get("channel")
    channel_id = "carpooling"

    # Case by case treatment of user requests
    cleaned_input = text.lower()
    if cleaned_input == "register":
        # update table
        df_new = df_new.append(pd.DataFrame([[name, "Y", "9-10", "Ste-Rose", 45.6160, -73.5900]], columns=df.columns))
        slack_web_client.api_call("chat.postMessage", channel=channel_id, text=tabulate(df_new, showindex="never", headers=df.columns, tablefmt="simple"))
        slack_web_client.api_call("chat.postMessage", channel=channel_id, text=f"\n{name} you've been added!")
    
    if cleaned_input == "request ride":
        #TODO DISTANCE
        pass

    if cleaned_input == "modify":
        slack_web_client.api_call("chat.postMessage", channel=channel_id, text=f"{name} is being modified.")
    
    if cleaned_input == "view passengers":
        slack_web_client.api_call("chat.postMessage", channel=channel_id, text=tabulate(df_new[df_new['Driver'] == "N"], showindex="never", headers=df.columns, tablefmt="simple"))
    
    if cleaned_input == "view drivers":
        slack_web_client.api_call("chat.postMessage", channel=channel_id, text=tabulate(df_new[df_new['Driver'] == "Y"], showindex="never", headers=df.columns, tablefmt="simple"))

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run(port=5000)