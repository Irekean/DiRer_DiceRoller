# Discord-Dice-Roller

# bot.py
The main Discord bot used to roll dices for tabletop games - WIP

# dice.py
The codes where the rolls are made, for now it uses everytime the actual timestamp as seed, in future will change in a similar way on how random.org works

# log.py
A simple console logger for the bot side

# readme.txt
A file like that should be created and put there just the bot token



# Dice Roller

A simple discord bot made to roll randomly virtual dices.

### Prerequisites

Python 3+

### Installing

Clone the repository where you want to start your bot, after installing python 3 install the dependency in Linux / Mac:

```
$ pip3 install -r requirements.txt
```

Or in Windows

```
> pip install -r requirements.txt
```

Then create and edit a new file named token.txt, paste in it your bot token taken from the discord developer portal website.

Finally you can start the bot:

Linux:
```
$ python3 bot.py
```
Windows:
```
> python bot.py
```

## Built With

* [Discord.py](https://pypi.org/project/discord.py/) - The official API class

## Authors

* **Fulvio Gambelli** - *The only developer* - [Linkedin](https://linkedin.com/in/fulviogambelli)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
