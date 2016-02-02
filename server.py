# channels.mark
# Sets the read cursor in a channel.

# channels.setPurpose
# Sets the purpose for a channel.

# channels.setTopic
# Sets the topic for a channel.

# chat.postMessage
# Sends a message to a channel

"""Server for the Pomotodo Game"""

from jinja2 import StrictUndefined

from flask import Flask, Markup, render_template, redirect, request, flash, session, jsonify, url_for, abort
from flask_debugtoolbar import DebugToolbarExtension

import time

from slacker import Slacker

from secrets import SLACK_BOT_API_TOKEN, FLASK_SECRET_KEY

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = FLASK_SECRET_KEY
slack = Slacker(SLACK_BOT_API_TOKEN)

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

CURRENT = ''

# Functions not associated with particular routes
#################################################################################

def create_pomo(length=25):
    slack.chat.post_message('#general', 'Got it! Starting a {}-minute pomodoro.'.format(length))
    time.sleep(length * 60)
    slack.chat.post_message('#general', 'Your {}-minute pomodoro is complete.'.format(length))

def check_messages(CURRENT):
    history = slack.channels.history('C0K0D3QHZ', count=1)
    messages = history.body['messages']

    for msg in messages:
        if msg['type'] == 'message':
            words = msg['text'].split()
            for word in words:
                if word == 'pomobot' and msg != CURRENT:
                    create_pomo()
                    return msg

#################################################################################

# TODO: Use Flask Login

while True:
    CURRENT = check_messages(CURRENT)
    time.sleep(1)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()


# # Send a message to #general channel
# slack.chat.post_message('#general', 'Hello fellow slackers!', as_user=True)

# # Get users list
# response = slack.users.list()
# users = response.body['members']

# # Upload a file
# slack.files.upload('hello.txt')