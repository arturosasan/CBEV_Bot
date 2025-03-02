CBEV Telegram Bot

Overview

The WTCBEV Telegram Bot is designed to manage and coordinate basketball training sessions and league matches. It provides automated surveys for training attendance and match availability, ensuring smooth team communication.

Features

1. Start Command (/start)

Initializes the bot.

Saves the group chat ID for future automated messages.

Replies with a welcome message explaining the bot's functionality.

2. Training Polls

Automatically sends training availability polls for Monday and Wednesday sessions.

Commands:

/MON - Sends a poll for Monday's training session.

/WEN - Sends a poll for Wednesday's training session.

Poll includes:

Attendance options: "Yes", "No", "Coach"

Training details: Date, time, and location

3. Match Polls

Sends availability polls for upcoming league matches.

Commands for Team A matches:

/JORN_A_17 - Matchday 17

/JORN_A_18 - Matchday 18

/JORN_A_19 - Matchday 19

/JORN_A_20 - Matchday 20

/JORN_A_21 - Matchday 21

/JORN_A_22 - Matchday 22

Commands for Team B matches:

/JORN_B_17 - Matchday 17

/JORN_B_18 - Matchday 18

/JORN_B_19 - Matchday 19

/JORN_B_20 - Matchday 20

/JORN_B_21 - Matchday 21

/JORN_B_22 - Matchday 22

Poll includes:

Attendance options: "Yes", "No", "Available", "Coach"

Match details: Date, opponent, time, and meeting point

Setup

1. Installation

Ensure you have Python installed, then install required dependencies:

pip install python-telegram-bot

2. Configuration

Replace TOKEN in the script with your Telegram bot token.

Start the bot using:

python bot.py

Notes

Training polls are sent only when explicitly triggered using /MON and /WEN.

Match polls are only sent when requested via their specific commands.

The bot does not send responses back to a private chat; all interactions occur within the group chat.

Author

Developed by @arturosasan
