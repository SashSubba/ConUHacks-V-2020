class carpoolRequest:
    BLOCK = {
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

    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "carpoolbot"
        self.icon_emoji = ":tada:"
        self.timestamp = ""

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.DIVIDER_BLOCK,
                self.BLOCK,
                self.DIVIDER_BLOCK,
            ],
        }
