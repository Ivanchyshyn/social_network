## GENERAL
This is test task for Python Developer in StarNavi.\
Main usage - creating and liking user posts.

## INSTALLING
### INITIAL
```
# setting env variables (default)
cp .env-example > .env

python3 -m venv venv
. venv/bin/activate
python -m pip install -r requirements.txt
```

### DATABASE
```
./initialize_database.sh
```

### BOT
Bot is a script, that creates users, posts and likes them.\
Bot configuration is in <i>bot_config.ini</i>.\
To run the bot, start the API server and execute this command:
```
python bot.py
```
