from dotenv import load_dotenv
from os.path import join, dirname
import os
import random
import requests

# Load the keys.env file
dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
giphy_key = os.getenv('GIPHY_KEY')

class Bot:
    def __init__(self, message):
        self.message = message
        
    def botResponses(self):
        message = self.message
        
        # Bot outputs about message
        if (message == '!!about' or message == '!! about'):
            message = 'This be a pirate themed chat app with many capabilities, to be sure! Explore away!'
            return message

        # Bot outputs help message showing known commands 
        elif (message == '!!help' or message == '!! help'):
            message = "Here be th' known commands ye can use: !!about - !!help - !!pirate - !!mood - !!famous - !!funtranslate <message> - !!insult - !!gif <message>"
            return message

        # Bot outputs definition of a pirate (got from urban dictionary)
        elif (message == '!!pirate' or message == '!! pirate'):
            message = 'A guy who drives a ship and yells "yo dude gimme your money and stuff" and gets whatever he wants. Usually has a stash or rum for some reason.'
            return message

        # Bot outputs a random mood
        elif (message == '!!mood' or message == '!! mood'):
            moods = ["I be feelin' like crackin' Jenny's tea cup.",
                    "I be feelin' ho.",
                    "I be feelin' marooned.",
                    "I be feelin' like committin piracy.",
                    "I be feelin' like taking a caulk.",
                    "I be feelin' angry.",
                    "I be feelin' like givin' no quarter.",
                    "I be feelin' like bringin' a spring upon her cable.",
                    "I be feelin' to blow the man down.",
                    "I be feelin' like parleying.",
                    "I be feelin' like drinkin' a simple grog."]
            message = random.choice(moods)
            return message

        # Bot outputs a random famous pirate
        elif (message == '!!famous' or message == '!! famous'):
            famousPirates = ['Anne Bonny was a famous pirate.',
                            'Bartholomew Roberts was a famous pirate.',
                            'Benjamin Hornigold was a famous pirate.',
                            'Blackbeard was a famous pirate.',
                            'Calico Jack was a famous pirate.',
                            'Charles Vane was a famous pirate.',
                            'Cheung Po Tsai was a famous pirate.',
                            'Edward England was a famous pirate.',
                            'Edward Low was a famous pirate.',
                            'Grace OMalley was a famous pirate.',
                            'Henry Every was a famous pirate.',
                            'Howell Davis was a famous pirate.',
                            'Mary Read was a famous pirate.',
                            'Paulsgrave Williams was a famous pirate.',
                            'Samuel Bellamy was a famous pirate.',
                            'Stede Bonnet was a famous pirate.',
                            'Thomas Tew was a famous pirate.',
                            'Turgut Reis was a famous pirate.',
                            'William Kidd was a famous pirate.',
                            'Sayyida al Hurra was a famous pirate.',
                            'Emanuel Wynn was a famous pirate.',
                            'Peter Easton was a famous pirate.',
                            'Richard Worley was a famous pirate.',
                            'Ching Shih was a famous pirate.',
                            'Christopher Contend was a famous pirate.',
                            'Christopher Moody was a famous pirate.']
            message = random.choice(famousPirates)
            return message

        # Bot translates any phrase you want into pirate lingo via API call
        elif (message.split()[0] == '!!funtranslate' or [message[i: i + 15] for i in range(0, len(message), 15)][0] == '!! funtranslate'):
            phrase = message[15:]
            api_link1 = f'https://api.funtranslations.com/translate/pirate.json?text={phrase}'
            parse_data1 = requests.get(api_link1).json()
            
            if 'success' in parse_data1:
                translation = parse_data1['contents']['translated']
                return translation
            else:
                message = 'Too Many Requests: Rate limit of 5 requests per hour exceeded.'
                return message

        # Bot displays a random pirate insult via API call
        elif (message == '!!insult' or message == '!! insult'):
            api_link2 = 'https://api.fungenerators.com/pirate/generate/insult?limit=5'
            parse_data2 = requests.get(api_link2).json()
            
            if 'success' in parse_data2:
                insults = parse_data2['contents']['taunts']
                message = random.choice(insults)
                return message
            else:
                message = 'Too Many Requests: Rate limit of 5 requests per day exceeded.'
                return message
        
        # Bot displays a gif of the word you inputted
        elif (message.split()[0] == '!!gif' or [message[i: i + 6] for i in range(0, len(message), 6)][0] == '!! gif'):
            word = message[6:]
            api_link3 = f'https://api.giphy.com/v1/gifs/search?api_key={giphy_key}&limit=1&q={word}'
            parse_data3 = requests.get(api_link3).json()
            
            if parse_data3['meta']['status'] != 200:
                message = 'Too Many Requsts: Rate limit of 42 searches per hour or 1000 searches per day exceeded.'
                return message
            elif parse_data3['pagination']['total_count'] == 0:
                message = 'Could not find a related gif.'
                return message
            else:
                gif = parse_data3['data'][0]['images']['downsized']['url']
                return gif

        # If unknown command, display this
        else:
            message = "Sorry, I dern't recognize that command. Please enter '!!help' to see a list o' commands."
            return message
            