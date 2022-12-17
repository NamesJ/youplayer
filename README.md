# YouPlayer
A collaborative YouTube music player

Automatically download and extract audio from YouTube videos shared via Telegram bot and play with VLC media player.

## Setup
### Notes
*You must have VLC installed for the program to work.*

*Currently, only Windows is supported.*
### Steps
1. Clone repo `git clone https://github.com/NamesJ/youplayer.git`
2. CD into repo `cd youplayer`
3. Create virtual environment `python -m venv venv`
4. Active venv `.\venv\scripts\activate`
5. Install required packages `pip install -r requirements.txt`
6. Copy `example.env` file to `.env`
7. Create a Telegram bot to get your API key
8. Replace example `API_KEY` value in `.env` with your bot API key
9. Run `main.py` to start the program
10. Start a conversation in Telegram with your bot
11. In Telegram, run bot command `/show_id` to get the chat ID for your account
12. Replace example `SUPER_CHAT_ID` value in `.env` with your chat ID. This will give your account all available permissions

## Usage
### Allow other users to add songs
1. Get chat IDs for users you wish to add (hint: they can use `/show_id` command to get their ID)
2. In Telegram, run bot command `/whitelist` and pass one or more of these chat IDs (example: `/whitelist 1111111111 2222222222` )

### Telegram bot commands (music player controls, adding songs)
To view a list of available commands send `/help` command to bot

## Notes
`youplayer.musicplayer` package not used in current version