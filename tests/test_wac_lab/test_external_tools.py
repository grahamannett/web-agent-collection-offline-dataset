import unittest
from unittest.mock import patch

from wac_lab.external_tools.cohere_api import generate_from_cohere
from wac_lab.external_tools.generate import generate_objective


class TestGenerateObjective(unittest.IsolatedAsyncioTestCase):
    # @patch("wac_lab.external_tools.cohere_api.requests.post")
    # def test_generate_objective_default_provider(self, mock_post):
    async def test_generate_objective_default_provider(self):
        # Mock the API response
        # mock_post.return_value.json.return_value = {
        #     "text": "Look up recipes for Sachertorte.\nConvert 100 GBP to AUD for a vacation budget.\nWhat is the etymology of the word 'serendipity'."
        # }
        result = generate_objective()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    @patch("wac_lab.external_tools.cohere_api.requests.post")
    def test_generate_objective_specific_provider(self, mock_post):
        # Mock the API response
        mock_post.return_value.json.return_value = {
            "text": "Look up recipes for Sachertorte.\nConvert 100 GBP to AUD for a vacation budget.\nWhat is the etymology of the word 'serendipity'."
        }
        result = generate_objective("cohere")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_generate_objective_invalid_provider(self):
        with self.assertRaises(KeyError):
            generate_objective("invalid_provider")


if __name__ == "__main__":
    unittest.main()
