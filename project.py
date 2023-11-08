import os
from string import Template

class Task:
    def __init__(self, task_id, instructions, consumed_variables=None, created_variables=None):
        self.task_id = task_id
        self.instructions = instructions
        self.consumed_variables = consumed_variables or []
        self.created_variables = created_variables or []
        self.status = 'incomplete'

class ProjectAssistant:
    def __init__(self):
        self.tasks = {}
        self.task_variables = {}

    def add_task(self, task_id, description, consumed_variables=None, created_variables=None):
        if task_id in self.tasks:
            raise KeyError(f"A task with ID {task_id} already exists.")
        self.tasks[task_id] = Task(task_id, description, consumed_variables, created_variables)
        self.task_variables[task_id] = {}

    def update_task_status(self, task_id, status):
        if task_id not in self.tasks:
            raise KeyError(f"No task with ID {task_id} exists.")
        self.tasks[task_id].status = status

    def add_task_variable(self, task_id, variable_name, variable_value):
        if task_id not in self.task_variables:
            raise KeyError(f"No task with ID {task_id} exists.")
        self.task_variables[task_id][variable_name] = variable_value

    def get_task_variables(self, task_id):
        if task_id not in self.task_variables:
            raise KeyError(f"No task with ID {task_id} exists.")
        return self.task_variables[task_id]

    def execute_task(self, task_id, execute_func, *args, **kwargs):
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
        documentation_contents = []
        for file_name in os.listdir(doc_folder_path):
            file_path = os.path.join(doc_folder_path, file_name)
            with open(file_path, 'r') as file:
                documentation_contents.append(file.read())
        return documentation_contents

    def fill_template_and_add_task(self, task_id, template_string, variables):
        template = Template(template_string)
        filled_template = template.substitute(variables)
        self.add_task(task_id, filled_template)
        return None

    def execute_and_prioritize_tasks(self):
        for task_id, task in self.tasks.items():
            if task.status != 'completed':
                self.execute_task(task_id, task.instructions)
                break
        return None