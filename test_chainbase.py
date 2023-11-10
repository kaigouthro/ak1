import unittest
from unittest.mock import patch, MagicMock
from chainbase import WebScraperAgent, CodeRefactorerAgent

class TestWebScraperAgent(unittest.TestCase):
    @patch('chainbase.save_as_markdown')
    @patch('chainbase.LangChain')
    def test_scrape_and_save_as_markdown(self, mock_lc, mock_save_as_markdown):
        mock_lc.ask.return_value = {'text': 'mocked text'}
        mock_save_as_markdown.return_value = 'mocked markdown'
        agent = WebScraperAgent()
        agent.scrape_and_save_as_markdown('mocked query')
        mock_lc.ask.assert_called_once_with('mocked query', agent="search_engine")
        mock_save_as_markdown.assert_called_once_with('mocked text')

class TestCodeRefactorerAgent(unittest.TestCase):
    @patch('chainbase.LangChain')
    def test_refactor_and_rewrite_code(self, mock_lc):
        mock_lc.get_prompt.return_value = 'mocked prompt'
        mock_lc.ask.return_value = {'text': 'mocked text'}
        agent = CodeRefactorerAgent()
        result = agent.refactor_and_rewrite_code('mocked code')
        self.assertEqual(result, 'mocked text')
        mock_lc.get_prompt.assert_any_call("Refactor code", {"code": 'mocked code'}, [], prompt_library=PromptLibrary())
        mock_lc.get_prompt.assert_any_call("Rewrite code", {"code": 'mocked text'}, [], prompt_library=PromptLibrary())
        self.assertEqual(mock_lc.ask.call_count, 2)

if __name__ == '__main__':
    unittest.main()
