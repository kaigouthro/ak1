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
    
    def __repr__(self):
        return f"Assistant(models={self.models}, tools={self.tools})"
