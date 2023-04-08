# RadioCord

A radio for discord voice chats. This bot plays music from internet radio live streams. 

## Try RadioCord
You can invite RadioCord to your server and try it out! - [RadioCord](https://discord.com/api/oauth2/authorize?client_id=1070962830381162526&permissions=3148032&scope=bot "RadioCord Invite Link")

## Getting started

### Requirements:
We are using [PyCord](https://github.com/Pycord-Development/pycord) instead of Discord.py for slash command support.

    python3 -m pip install -U "py-cord[voice]"


youtube-dl for the lofi & youtube sections. (this is now disabled by default)

    sudo pip install --upgrade youtube_dl

Also requires `FFMPEG` for the radio module. 

### Setup
Visit the [developer portal](https://discord.com/developers/applications) and create a bot token and invite link. 

Under `Bot` select all three Privileged Gateway Intents

Under `OAuth2` then `URL Generator` select `bot`. 

Next select the following permissions:
- Send Message
- Voice Connect
- Voice Speak
- Voice Priority Speaker (optional)

Use the generated link to import your bot into your discord server. 

Finally create a new file named `token.secret` and place the bot token inside that file. 

Run the bot `python3 radiocord.py`

## Usage

Once radiocord is running you can use slash commands to launch the available radio stations. You must be connected to a voice channel before launching the bot. Currently it does not leave unless the /leave command is used. 