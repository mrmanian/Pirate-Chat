""" Import required modules """
import os
from os.path import join, dirname
import random
from dotenv import load_dotenv
import requests

# Load the keys.env file
dotenv_path = join(dirname(__file__), "keys.env")
load_dotenv(dotenv_path)
giphy_key = os.getenv("GIPHY_KEY")


class Bot:
    """ Class Bot """

    def __init__(self, message):
        self.message = message

    def bot_responses(self):
        """ Bot commands """
        message = self.message

        # Bot outputs about message
        if (
            message.split()[0] == "!!about"
            or [message[i : i + 8] for i in range(0, len(message), 8)][0] == "!! about"
        ):

            if message.split("about", 1)[1] not in "":
                message = "Don't enter anything after '!!about'"
                return message
            message = "This be a pirate themed chat app with many capabilities, \
                      to be sure! Explore away!"
            return message

        # Bot outputs help message showing known commands
        if (
            message.split()[0] == "!!help"
            or [message[i : i + 7] for i in range(0, len(message), 7)][0] == "!! help"
        ):

            if message.split("help", 1)[1] not in "":
                message = "Don't enter anything after '!!help'"
                return message
            message = "Here be th' known commands ye can use: !!about - !!help - !!pirate \
                       - !!mood - !!famous - !!funtranslate <message> - !!insult - !!gif <message>"
            return message

        # Bot outputs definition of a pirate (got from urban dictionary)
        if (
            message.split()[0] == "!!pirate"
            or [message[i : i + 9] for i in range(0, len(message), 9)][0] == "!! pirate"
        ):

            if message.split("pirate", 1)[1] not in "":
                message = "Don't enter anything after '!!pirate'"
                return message
            message = 'A guy who drives a ship and yells "yo dude gimme your money and stuff" \
                      and gets whatever he wants. Usually has a stash or rum for some reason.'
            return message

        # Bot outputs a random mood
        if (
            message.split()[0] == "!!mood"
            or [message[i : i + 7] for i in range(0, len(message), 7)][0] == "!! mood"
        ):

            if message.split("mood", 1)[1] not in "":
                message = "Don't enter anything after '!!mood'"
                return message
            moods = [
                "I be feelin' like crackin' Jenny's tea cup.",
                "I be feelin' ho.",
                "I be feelin' marooned.",
                "I be feelin' like committin piracy.",
                "I be feelin' like taking a caulk.",
                "I be feelin' angry.",
                "I be feelin' like givin' no quarter.",
                "I be feelin' like bringin' a spring upon her cable.",
                "I be feelin' to blow the man down.",
                "I be feelin' like parleying.",
                "I be feelin' like drinkin' a simple grog.",
            ]
            message = random.choice(moods)
            return message

        # Bot outputs a random famous pirate
        if (
            message.split()[0] == "!!famous"
            or [message[i : i + 9] for i in range(0, len(message), 9)][0] == "!! famous"
        ):

            if message.split("famous", 1)[1] not in "":
                message = "Don't enter anything after '!!famous'"
                return message
            famous_pirates = [
                "Anne Bonny was a famous pirate.",
                "Bartholomew Roberts was a famous pirate.",
                "Benjamin Hornigold was a famous pirate.",
                "Blackbeard was a famous pirate.",
                "Calico Jack was a famous pirate.",
                "Charles Vane was a famous pirate.",
                "Cheung Po Tsai was a famous pirate.",
                "Edward England was a famous pirate.",
                "Edward Low was a famous pirate.",
                "Grace OMalley was a famous pirate.",
                "Henry Every was a famous pirate.",
                "Howell Davis was a famous pirate.",
                "Mary Read was a famous pirate.",
                "Paulsgrave Williams was a famous pirate.",
                "Samuel Bellamy was a famous pirate.",
                "Stede Bonnet was a famous pirate.",
                "Thomas Tew was a famous pirate.",
                "Turgut Reis was a famous pirate.",
                "William Kidd was a famous pirate.",
                "Sayyida al Hurra was a famous pirate.",
                "Emanuel Wynn was a famous pirate.",
                "Peter Easton was a famous pirate.",
                "Richard Worley was a famous pirate.",
                "Ching Shih was a famous pirate.",
                "Christopher Contend was a famous pirate.",
                "Christopher Moody was a famous pirate.",
            ]
            message = random.choice(famous_pirates)
            return message

        # Bot translates any phrase you want into pirate lingo via API call
        if (
            message.split()[0] == "!!funtranslate"
            or [message[i : i + 15] for i in range(0, len(message), 15)][0]
            == "!! funtranslate"
        ):

            phrase = message[15:]
            if phrase == "":
                message = "Enter a word or phrase to translate after '!!funtranslate'"
                return message
            api_link1 = (
                f"https://api.funtranslations.com/translate/pirate.json?text={phrase}"
            )
            parse_data1 = requests.get(api_link1)

            if parse_data1.status_code == 200:
                parse_data1 = parse_data1.json()
                translation = parse_data1["contents"]["translated"]
                return translation
            message = "Too Many Requests: Rate limit of 5 requests per hour exceeded."
            return message

        # Bot displays a random pirate insult via API call
        if (
            message.split()[0] == "!!insult"
            or [message[i : i + 9] for i in range(0, len(message), 9)][0] == "!! insult"
        ):

            if message.split("insult", 1)[1] not in "":
                message = "Don't enter anything after '!!insult'"
                return message
            api_link2 = "https://api.fungenerators.com/pirate/generate/insult?limit=5"
            parse_data2 = requests.get(api_link2)

            if parse_data2.status_code == 200:
                parse_data2 = parse_data2.json()
                insults = parse_data2["contents"]["taunts"]
                message = random.choice(insults)
                return message
            message = "Too Many Requests: Rate limit of 5 requests per day exceeded."
            return message

        # Bot displays a gif of the word you inputted
        if (
            message.split()[0] == "!!gif"
            or [message[i : i + 6] for i in range(0, len(message), 6)][0] == "!! gif"
        ):

            word = message[6:]
            if word == "":
                message = "Enter a word or phrase after '!!gif'"
                return message
            api_link3 = f"https://api.giphy.com/v1/gifs/search?api_key={giphy_key}&limit=1&q={word}"
            parse_data3 = requests.get(api_link3)

            if parse_data3.status_code == 200:
                parse_data3 = parse_data3.json()
                if parse_data3["pagination"]["total_count"] == 0:
                    message = "Could not find a related gif."
                    return message
                gif = parse_data3["data"][0]["images"]["downsized"]["url"]
                return gif
            message = "Too Many Requests: Rate limit of 42 searches per hour or 1000 searches \
                        per day exceeded."
            return message

        # Bot displays error if user inputs unrecognized command
        message = "Sorry, I dern't recognize that command. Please enter '!!help' \
                  to see a list o' commands."
        return message
