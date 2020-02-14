# How to set up the Bot

## Optain Reddit oAuth credentials
* go to https://www.reddit.com/prefs/apps
* Create a new application and note down the id and the secret for later use

## Add a Webhook on a server
* In the Discord Client go to 'Server Settings'
* Go to Section 'Webhook'
* Create a new Webhook. Specify name and channel and copy the Link for the next step

## Setup the environment
* Create a `.env` file containing the key value pairs from the `dotenv_template` file.
* Substitute with the values obtained from the previous steps.
* Add the name of a subreddit.

For the following steps make sure the python version used is 3.7. Otherwise Pipenv will scream at you.
* install pipenv `python -m pip install`.
* create the shell `pipenv shell` this will also load the values of the created `.env` file.
* run `pipenv install --ignore-pipfile` this will install the exact dependencies from the lockfile.

Now you can run the bot with `python server.py`

In it's current iteration it will query the specified subreddit every 15 minutes and post all new submissions to the specified webhook.