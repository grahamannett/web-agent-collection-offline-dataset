import unittest
from unittest.mock import patch

from wac_lab.external_tools.cohere_api import generate_from_cohere
from wac_lab.external_tools.generate import generate_objective


mock_response = (
    "Search for the best noise-cancelling headphones.\n"
    "Check the weather forecast for the upcoming week.\n"
    "Find and compare local restaurant reviews.\n"
    "Book a hotel room for a weekend getaway.\n"
    "Research and apply for a new credit card."
)


class TestGenerateObjective(unittest.IsolatedAsyncioTestCase):
    @patch("wac_lab.external_tools.cohere_api.requests.post")
    async def test_generate_objective_default_provider(self, mock_post):
        mock_post.return_value.json.return_value = {"text": mock_response}
        result = generate_objective()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    @patch("wac_lab.external_tools.cohere_api.requests.post")
    def test_generate_objective_specific_provider(self, mock_post):
        mock_post.return_value.json.return_value = {"text": mock_response}
        result = generate_objective(provider="cohere")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_generate_objective_invalid_provider(self):
        with self.assertRaises(KeyError):
            generate_objective("invalid_provider")


if __name__ == "__main__":
    unittest.main()
