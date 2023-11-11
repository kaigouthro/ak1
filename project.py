import os
import heapq
from string import Template

class Task:
    def __init__(self, task_id, instructions, consumed_variables=None, created_variables=None, priority=0, dependencies=None):
        self.task_id = task_id
        self.instructions = instructions
        self.consumed_variables = consumed_variables or []
        self.created_variables = created_variables or []
        self.priority = priority
        self.dependencies = dependencies or []
        self.status = 'incomplete'

class ProjectAssistant:
    def __init__(self):
        self.tasks = []
        self.task_variables = {}

    def add_task(self, task_id, description, consumed_variables=None, created_variables=None, priority=0, dependencies=None):
        if any(task.task_id == task_id for _, task in self.tasks):
            raise KeyError(f"A task with ID {task_id} already exists.")
        task = Task(task_id, description, consumed_variables, created_variables, priority, dependencies)
        heapq.heappush(self.tasks, (priority, task))
        self.task_variables[task_id] = {}

    def update_task_status(self, task_id, status):
        for _, task in self.tasks:
            if task.task_id == task_id:
                task.status = status
                return
        raise KeyError(f"No task with ID {task_id} exists.")

    def add_task_variable(self, task_id, variable_name, variable_value):
        if task_id not in self.task_variables:
            raise KeyError(f"No task with ID {task_id} exists.")
        self.task_variables[task_id][variable_name] = variable_value

    def get_task_variables(self, task_id):
        if task_id not in self.task_variables:
            raise KeyError(f"No task with ID {task_id} exists.")
        return self.task_variables[task_id]

    def execute_task(self, task_id, execute_func, *args, **kwargs):
        for _, task in self.tasks:
            if task.task_id == task_id:
                consumed_variables = {}
                for variable in task.consumed_variables:
                    if variable not in kwargs:
                        raise ValueError(f"Missing variable '{variable}' for task execution.")
                    consumed_variables[variable] = kwargs[variable]
                try:
                    result = execute_func(*args, **consumed_variables)
                except Exception as e:
                    raise ValueError(f"Error executing task {task_id}: {str(e)}")
                created_variables = {variable: result[variable] for variable in task.created_variables}
                kwargs.update(created_variables)
                self.task_variables[task_id] = created_variables
                return result
        raise KeyError(f"No task with ID {task_id} exists.")

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

    def execute_tasks_based_on_dependencies(self):
        while self.tasks:
            for i, (priority, task) in enumerate(self.tasks):
                if all(dependency.status == 'completed' for dependency in task.dependencies):
                    self.execute_task(task.task_id, task.instructions)
                    break
            else:
                raise ValueError("Cannot execute any more tasks due to unmet dependencies.")
            del self.tasks[i]

# Add tasks related to Langchain integration to the ProjectAssistant instance
project_assistant = ProjectAssistant()
project_assistant.add_task('langchain_integration', 'Integrate Langchain OpenAI into the existing codebase.')
project_assistant.add_task('expand_chainbase', 'Expand the chainbase.py file to include more functionalities using Langchain OpenAI.')
project_assistant.add_task('create_langchain_runnables', 'Create Langchain runnables for efficient execution of tasks.')