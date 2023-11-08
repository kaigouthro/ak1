class Template:
    def __init__(self, template_string):
        self.template_string = template_string

    def fill_template(self, variables):
        """
        Fill the template string with the given variables.

        Args:
            variables (dict): A dictionary containing variable names as keys and their respective values.

        Returns:
            str: The template string with variables replaced by their values.
        """
        filled_template = self.template_string
        for variable_name, variable_value in variables.items():
            filled_template = filled_template.replace(f"${variable_name}", str(variable_value))
        return filled_template


class Task:
    def __init__(self, task_id, instructions, consumed_variables=None, created_variables=None):
        self.task_id = task_id
        self.instructions = instructions
        self.consumed_variables = consumed_variables or []
        self.created_variables = created_variables or []

class ProjectAssistant:
    def __init__(self):
        self.tasks = {}
        self.task_variables = {}

    def add_task(self, task_id, description, consumed_variables=None, created_variables=None):
        """
        Add a new task to the project.

        Args:
            task_id (str): The unique identifier of the task.
            description (str): The description of the task.
            consumed_variables (list): A list of variables consumed by the task. (optional)
            created_variables (list): A list of variables created by the task. (optional)
        """
        if task_id in self.tasks:
            raise KeyError(f"A task with ID {task_id} already exists.")
        self.tasks[task_id] = Task(task_id, description, consumed_variables, created_variables)
        self.task_variables[task_id] = {}

    def update_task_status(self, task_id, status):
        """
        Update the status of a task.

        Args:
            task_id (str): The unique identifier of the task.
            status (str): The new status of the task.
        """
        if task_id not in self.tasks:
            raise KeyError(f"No task with ID {task_id} exists.")
        self.tasks[task_id].status = status

    def add_task_variable(self, task_id, variable_name, variable_value):
        """
        Add a variable to a task's variables.

        Args:
            task_id (str): The unique identifier of the task.
            variable_name (str): The name of the variable.
            variable_value (any): The value of the variable.
        """
        if task_id not in self.task_variables:
            raise KeyError(f"No task with ID {task_id} exists.")
        self.task_variables[task_id][variable_name] = variable_value

    def get_task_variables(self, task_id):
        """
        Retrieve the variables of a completed task.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            dict: A dictionary containing the variables of the task.
        """
        if task_id not in self.task_variables:
            raise KeyError(f"No task with ID {task_id} exists.")
        return self.task_variables[task_id]

    def execute_task(self, task_id, execute_func, *args, **kwargs):
        """
        Execute the specified task.

        Args:
            task_id (str): The unique identifier of the task.
            execute_func (callable): The function to execute for the task.
            *args: Additional positional arguments to pass to the execute function.
            **kwargs: Additional keyword arguments to pass to the execute function.

        Returns:
            Any: The result of executing the task.
        """
        if task_id not in self.tasks:
            raise KeyError(f"No task with ID {task_id} exists.")
        task = self.tasks[task_id]

        consumed_variables = {}
        for variable in task.consumed_variables:
            if variable not in kwargs:
                raise ValueError(f"Missing variable '{variable}' for task execution.")
            consumed_variables[variable] = kwargs[variable]

        result = execute_func(*args, **consumed_variables)

        created_variables = {variable: result[variable] for variable in task.created_variables}
        kwargs.update(created_variables)

        self.task_variables[task_id] = created_variables

        return result

    def read_documentation(self, doc_folder_path):
        """
        Read and process documentation files from the specified folder.

        Args:
            doc_folder_path (str): The path to the folder containing documentation files.

        Returns:
            list: A list of processed documentation contents.
        """
        # Placeholder logic for reading and processing documentation files
        documentation_contents = []
        for file_name in os.listdir(doc_folder_path):
            file_path = os.path.join(doc_folder_path, file_name)
            with open(file_path, 'r') as file:
                documentation_contents.append(file.read())
        return documentation_contents

    def read_write_execute_code(self, file_name, code):
        """
        Read, write, and execute code.

        Args:
            file_name (str): The name of the code file to interact with.
            code (str): The code to execute.

        Returns:
            Any: The result of executing the code.
        """
        # Placeholder logic for reading, writing, and executing code
        with open(file_name, 'w') as file:
            file.write(code)
        exec(code)  # Execute the code
        return None
