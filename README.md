# LibertyScore

# Twitter Bot - Liberty Score

This project is a Twitter bot that checks mentions of a specified politician and replies with their Liberty Score. The bot can be run in two modes:

- **Mock Mode**: Used for testing purposes with fake data (mocked mentions).
- **Real Mode**: Connects to the Twitter API to fetch real mentions and reply to them.

## Features

- Fetches mentions of the bot from Twitter (or uses mock mentions if in mock mode).
- Extracts the politician's name from the tweet.
- Retrieves the Liberty Score of the politician.
- Replies to the tweet with the politician's Liberty Score.
- Easy to toggle between mock mode and real mode.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- `pip` for package management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/twitter-bot-liberty-score.git
   cd twitter-bot-liberty-score

2. Install the required dependencies:

    '''bash
    Copy
    Edit
    pip install -r requirements.txt

3. Set up environment variables: You will need Twitter API keys to run the bot in real mode. Set up a .env file with the following keys:

    env
    Copy
    Edit
    API_KEY=your-api-key
    API_SECRET=your-api-secret
    ACCESS_TOKEN=your-access-token
    ACCESS_SECRET=your-access-secret
    

4. (Optional) To simulate the bot using mock data, you'll need a mock_mentions.json file containing sample tweet data.

## Usage  
Mock Mode
- Mock mode is useful for testing the bot without interacting with the real Twitter API.

- How to enable mock mode: Open bot.py and set MOCK_MODE = True.

- The bot will use the mock_mentions.json file for testing. Make sure you have a file with sample tweet data.

Real Mode
In real mode, the bot will fetch real mentions from Twitter and respond to them with Liberty Scores.

- How to enable real mode: Open bot.py and set MOCK_MODE = False.

- The bot will require Twitter API keys to function properly in real mode. Make sure you've set the environment variables in your .env file.

Running the Bot
1.  Ensure that the environment variables are set (either manually or via the .env file).

2.  Run the bot in Command window with:
python bot.py

## Files
- bot.py: The main bot script that fetches mentions and replies with Liberty Scores. It can operate in mock mode or real mode.

- mock_mentions.json: Sample data used for testing the bot in mock mode. This file contains a list of mocked tweets.

- twitter_api_wrapper.py: A custom wrapper for interacting with the Twitter API (either in mock or real mode).

- requirements.txt: List of required Python packages for the bot.