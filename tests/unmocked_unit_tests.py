""" Import required modules """
import unittest
from os.path import dirname, join
import sys

sys.path.append(join(dirname(__file__), "../"))
import chatbot
import app
import models


class UnmockedTests(unittest.TestCase):
    """ Unmocked Unit Tests """

    ABOUT = "!!about"
    HELP = "!!help"
    PIRATE = "!!pirate"
    INVALID_COMMAND = "!! jfsjfslf"


    def test_about_command(self):
        """ Mocked bot about command """
        captain = chatbot.Bot(UnmockedTests.ABOUT)
        expected = "This be a pirate themed chat app with many capabilities, \
                      to be sure! Explore away!"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_help_command(self):
        """ Mocked bot help command """
        captain = chatbot.Bot(UnmockedTests.HELP)
        expected = "Here be th' known commands ye can use: !!about - !!help - !!pirate \
                       - !!mood - !!famous - !!funtranslate <message> - !!insult - !!gif <message>"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_pirate_command(self):
        """ Mocked bot pirate command """
        captain = chatbot.Bot(UnmockedTests.PIRATE)
        expected = 'A guy who drives a ship and yells "yo dude gimme your money and stuff" \
                      and gets whatever he wants. Usually has a stash or rum for some reason.'
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid(self):
        """ Mocked bot invalid input """
        captain = chatbot.Bot(UnmockedTests.INVALID_COMMAND)
        expected = "Sorry, I dern't recognize that command. Please enter '!!help' \
                  to see a list o' commands."
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
