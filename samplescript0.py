msg = inputs["Slack_Message_Text"]
usr = inputs["Slack_User"]

outputs['Response Message'] = f'Hello {usr}, I have received your message \"{msg}\"'
