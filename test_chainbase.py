import unittest
from unittest.mock import patch, MagicMock
from chainbase import WebScraperAgent, CodeRefactorerAgent, LangchainAssistant

class TestChainbase(unittest.TestCase):
    @patch('chainbase.lc.ask')
    @patch('chainbase.save_as_markdown')
    def test_WebScraperAgent_scrape_and_save_as_markdown(self, mock_ask, mock_save_as_markdown):
        mock_ask.return_value = {'text': 'search results'}
        mock_save_as_markdown.return_value = 'markdown data'
        agent = WebScraperAgent()
        agent.scrape_and_save_as_markdown('search query')
        mock_ask.assert_called_once_with('search query', agent="search_engine")
        mock_save_as_markdown.assert_called_once_with('search results')

    @patch('chainbase.lc.get_prompt')
    @patch('chainbase.lc.ask')
    @patch('chainbase.PromptLibrary')
    def test_CodeRefactorerAgent_refactor_and_rewrite_code(self, mock_get_prompt, mock_ask, mock_PromptLibrary):
        mock_get_prompt.return_value = 'instructions'
        mock_ask.return_value = {'text': 'code'}
        agent = CodeRefactorerAgent()
        agent.refactor_and_rewrite_code('code')
        mock_get_prompt.assert_any_call("Refactor code", {"code": 'code'}, [], prompt_library=mock_PromptLibrary())
        mock_get_prompt.assert_any_call("Rewrite code", {"code": 'code'}, [], prompt_library=mock_PromptLibrary())
        mock_ask.assert_any_call('instructions', agent=LLM.queue)

    @patch('chainbase.WebScraperAgent.scrape_and_save_as_markdown')
    def test_LangchainAssistant_scrape_web_and_convert_to_markdown(self, mock_scrape_and_save_as_markdown):
        assistant = LangchainAssistant()
        assistant.scrape_web_and_convert_to_markdown('search query')
        mock_scrape_and_save_as_markdown.assert_called_once_with('search query')

    @patch('chainbase.CodeRefactorerAgent.refactor_and_rewrite_code')
    def test_LangchainAssistant_refactor_and_rewrite_code(self, mock_refactor_and_rewrite_code):
        assistant = LangchainAssistant()
        assistant.refactor_and_rewrite_code('code')
        mock_refactor_and_rewrite_code.assert_called_once_with('code')

if __name__ == '__main__':
    unittest.main()
