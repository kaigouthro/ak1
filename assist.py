class Assistant:
    """
    A class to represent an AI assistant equipped with various tools.
    
    Attributes:
    - models: a list of models that the assistant can access
    - tools: a list of tools the assistant has access to
    """
    
    def __init__(self, models=None, tools=None):
        """
        Initialize the assistant with the specified models and tools.
        """
        self.models = models if models is not None else []
        self.tools = tools if tools is not None else []
    
    def add_model(self, model):
        """
        Add a model to the assistant's list of models.
        """
        self.models.append(model)
    
    def add_tool(self, tool):
        """
        Add a tool to the assistant's list of tools.
        """
        self.tools.append(tool)
    
    def call_model(self, instruction):
        """
        Call a model with an instruction and return the model's output.
        """
        return "Model output for instruction: {}".format(instruction)
    
    def use_tool(self, tool_name, params):
        """
        Use a tool with the given parameters and return the tool's output.
        """
        return "Used tool {} with params: {}".format(tool_name, params)
    
    def scrape_web_and_save_markdown(self, search_query):
        """
        Perform web scraping and save data into markdown files.
        """
        # Placeholder logic for web scraping and markdown file creation
        web_data = self.use_tool('DuckDuckGo', {'query': search_query})
        markdown_data = convert_to_markdown(web_data)  # Placeholder function for converting web data to markdown
        with open(f"{search_query.replace(' ', '_')}.md", 'w') as file:
            file.write(markdown_data)
        return None
    
    def refactor_and_rewrite_code(self, code):
        """
        Refactor and rewrite code.
        """
        # Placeholder logic for code refactoring and rewriting
        refactored_code = self.use_tool('Sourcery', {'code': code})
        rewritten_code = self.call_model('GPT-3.5', {'code': refactored_code})
        return rewritten_code
    
    def format_response(self, response):
        """
        Format responses in a parseable manner.
        """
        # Placeholder logic for response formatting
        formatted_response = json.dumps(response)  # Convert response to JSON
        return formatted_response
    
    def __repr__(self):
        return f"Assistant(models={self.models}, tools={self.tools})"

class ProjectAssistant:
    """
    A class to represent a project assistant that can read, write, and execute code.
    """
    
    def read_write_execute_code(self, file_name, code):
        """
        Read, write, and execute code.
        """
        with open(file_name, 'w') as file:
            file.write(code)
        exec(code)  # Execute the code
        return None