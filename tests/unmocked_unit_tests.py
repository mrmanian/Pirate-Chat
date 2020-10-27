""" Import required modules """
import unittest
from os.path import dirname, join
import sys

sys.path.append(join(dirname(__file__), "../"))
import chatbot


class UnmockedTests(unittest.TestCase):
    """ Unmocked Unit Tests """

    ABOUT = "!!about"
    HELP = "!!help"
    PIRATE = "!!pirate"
    INVALID_COMMAND = "!! jfsjfslf"
    INVALID_ABOUT = "!!about word"
    INVALID_HELP = "!!help word"
    INVALID_PIRATE = "!!pirate word"
    INVALID_MOOD = "!!mood word"
    INVALID_FAMOUS = "!!famous word"
    INVALID_FUNTRANSLATE = "!!funtranslate"
    INVALID_INSULT = "!!insult word"
    INVALID_GIF = "!!gif"

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

    def test_invalid_about(self):
        """ Mocked bot invalid about command """
        captain = chatbot.Bot(UnmockedTests.INVALID_ABOUT)
        expected = "Don't enter anything after '!!about'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid_help(self):
        """ Mocked bot invalid help command """
        captain = chatbot.Bot(UnmockedTests.INVALID_HELP)
        expected = "Don't enter anything after '!!help'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid_pirate(self):
        """ Mocked bot invalid pirate command """
        captain = chatbot.Bot(UnmockedTests.INVALID_PIRATE)
        expected = "Don't enter anything after '!!pirate'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid_mood(self):
        """ Mocked bot invalid mood command """
        captain = chatbot.Bot(UnmockedTests.INVALID_MOOD)
        expected = "Don't enter anything after '!!mood'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid_famous(self):
        """ Mocked bot invalid famous command """
        captain = chatbot.Bot(UnmockedTests.INVALID_FAMOUS)
        expected = "Don't enter anything after '!!famous'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid_funtranslate(self):
        """ Mocked bot invalid funtranslate command """
        captain = chatbot.Bot(UnmockedTests.INVALID_FUNTRANSLATE)
        expected = "Enter a word or phrase to translate after '!!funtranslate'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid_insult(self):
        """ Mocked bot invalid insult command """
        captain = chatbot.Bot(UnmockedTests.INVALID_INSULT)
        expected = "Don't enter anything after '!!insult'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_invalid_gif(self):
        """ Mocked bot invalid gif command """
        captain = chatbot.Bot(UnmockedTests.INVALID_GIF)
        expected = "Enter a word or phrase after '!!gif'"
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
