# YouPlayer
A collaborative YouTube music player

Automatically download and extract audio from YouTube videos shared via Telegram bot and play with VLC media player.

## Setup
1. Copy `example.env` file to `.env`
2. Create a Telegram bot to get your API key
3. Replace example `API_KEY` value in `.env` with your bot API key
4. Run `main.py` to start the program
5. Start a conversation in Telegram with your bot
6. In Telegram, run bot command `/show_id` to get the chat ID for your account
7. Replace example `SUPER_CHAT_ID` value in `.env` with your chat ID. This will give your account all available permissions

## Setup (cont.) -- allows other users
1. Get chat IDs for users you wish to add (hint: they can use `/show_id` command to get their ID)
2. In Telegram, run bot command `/whitelist` and pass one or more of these chat IDs (example: `/whitelist 1111111111 2222222222` )


## Notes
`youplayer.musicplayer` package not used in current version