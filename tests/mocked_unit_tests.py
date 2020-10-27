""" Import required modules """
import unittest
import unittest.mock as mock
from unittest.mock import patch
from os.path import dirname, join
import sys
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

sys.path.append(join(dirname(__file__), "../"))
import chatbot
import app
import models


class MockedTests(unittest.TestCase):
    """ Mocked Unit Tests  """

    MOOD = "!!mood"
    FAMOUS = "!!famous"
    FUNTRANSLATE = "!!funtranslate sentence"
    INSULT = "!!insult"
    GIF = "!!gif word"

    @staticmethod
    def mocked_random_choice(value):
        """ Mocked random choice function """
        return value[0]

    def test_mood_command(self):
        """ Mocked bot mood command """
        captain = chatbot.Bot(MockedTests.MOOD)
        expected = "I be feelin' like crackin' Jenny's tea cup."
        with mock.patch("random.choice", self.mocked_random_choice):
            actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    def test_famous_command(self):
        """ Mocked bot famous command """
        captain = chatbot.Bot(MockedTests.FAMOUS)
        expected = "Anne Bonny was a famous pirate."
        with mock.patch("random.choice", self.mocked_random_choice):
            actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @mock.patch("chatbot.requests.get")
    def test_funtranslate_success_command(self, mock_requests_get):
        """ Mocked bot funtranslate success command """
        captain = chatbot.Bot(MockedTests.FUNTRANSLATE)
        expected = "Ahoy how be ye doin' today good matey"
        mock_requests_get.return_value = mock.Mock(
            **{
                "status_code": 200,
                "json.return_value": {
                    "contents": {"translated": "Ahoy how be ye doin' today good matey"}
                },
            }
        )
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @mock.patch("chatbot.requests.get")
    def test_funtranslate_failed_command(self, mock_requests_get):
        """ Mocked bot funtranslate failure command """
        captain = chatbot.Bot(MockedTests.FUNTRANSLATE)
        expected = "Too Many Requests: Rate limit of 5 requests per hour exceeded."
        mock_requests_get.return_value = mock.Mock(
            **{
                "status_code": 429,
                "json.return_value": {"contents": {"translated": ""}},
            }
        )
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @mock.patch("chatbot.requests.get")
    def test_insult_success_command(self, mock_requests_get):
        """ Mocked bot insult sucess command """
        captain = chatbot.Bot(MockedTests.INSULT)
        expected = (
            "Happy now? Ye have me FULL attention! ye el-smelling plundering matey!"
        )
        mock_requests_get.return_value = mock.Mock(
            **{
                "status_code": 200,
                "json.return_value": {
                    "contents": {
                        "taunts": [
                            "Happy now? Ye have me FULL attention! ye el-smelling plundering matey!"
                        ]
                    }
                },
            }
        )
        with mock.patch("random.choice", self.mocked_random_choice):
            actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @mock.patch("chatbot.requests.get")
    def test_insult_failed_command(self, mock_requests_get):
        """ Mocked bot insult failure command """
        captain = chatbot.Bot(MockedTests.INSULT)
        expected = "Too Many Requests: Rate limit of 5 requests per day exceeded."
        mock_requests_get.return_value = mock.Mock(
            **{"status_code": 429, "json.return_value": {"contents": {"taunts": [""]}}}
        )
        with mock.patch("random.choice", self.mocked_random_choice):
            actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @mock.patch("chatbot.requests.get")
    def test_gif_success_command(self, mock_requests_get):
        """ Mocked bot gif success command """
        captain = chatbot.Bot(MockedTests.GIF)
        expected = "https://gph.is/g/4g0e07A"
        mock_requests_get.return_value = mock.Mock(
            **{
                "status_code": 200,
                "json.return_value": {
                    "data": [
                        {"images": {"downsized": {"url": "https://gph.is/g/4g0e07A"}}}
                    ],
                    "pagination": {"total_count": 1},
                },
            }
        )
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @mock.patch("chatbot.requests.get")
    def test_gif_failed1_command(self, mock_requests_get):
        """ Mocked bot gif failure command """
        captain = chatbot.Bot(MockedTests.GIF)
        expected = "Could not find a related gif."
        mock_requests_get.return_value = mock.Mock(
            **{
                "status_code": 200,
                "json.return_value": {"data": [], "pagination": {"total_count": 0}},
            }
        )
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @mock.patch("chatbot.requests.get")
    def test_gif_failed2_command(self, mock_requests_get):
        """ Mocked bot gif failure command """
        captain = chatbot.Bot(MockedTests.GIF)
        expected = "Too Many Requests: Rate limit of 42 searches per hour or 1000 searches \
                        per day exceeded."
        mock_requests_get.return_value = mock.Mock(
            **{
                "status_code": 429,
                "json.return_value": {"data": [], "pagination": {"total_count": 0}},
            }
        )
        actual = captain.bot_responses()
        self.assertEqual(expected, actual)

    @patch("builtins.print")
    def test_on_connect(self, mock_print):
        """ Mocked socket connection print response """
        app.on_connect()
        mock_print.assert_called_with("Someone connected!")

    @patch("builtins.print")
    def test_on_disconnect(self, mock_print):
        """ Mocked socket disconnect print response """
        app.on_disconnect()
        mock_print.assert_called_with("Someone disconnected!")

    @patch("builtins.print")
    def test_on_logout(self, mock_print):
        """ Mocked logout print response """
        app.on_logout()
        mock_print.assert_called_with("Someone logged out!")

    @patch("flask.templating._render", return_value="")
    def test_mocked_render(self, mocked):
        """ Mocked flask render template response """
        test_client = app.app.test_client()
        test_client.get("/")
        self.assertEqual(mocked.called, True)

    def test_database_values(self):
        """ Mocked database initalization """
        session = UnifiedAlchemyMagicMock()
        session.add(
            models.ChatHistory(
                user_name="mike", pic_url="https://google.com", message="hi"
            )
        )
        query = session.query(models.ChatHistory).first()
        self.assertEqual(query.user_name, "mike")
        self.assertEqual(query.pic_url, "https://google.com")
        self.assertEqual(query.message, "hi")


if __name__ == "__main__":
    unittest.main()
