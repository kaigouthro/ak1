import unittest

import project


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project_assistant = project.ProjectAssistant()

    def test_add_task(self):
        self.project_assistant.add_task("task1", "description1")
        self.assertIn("task1", self.project_assistant.task_variables)

    def test_update_task_status(self):
        self.project_assistant.add_task("task1", "description1")
        self.project_assistant.update_task_status("task1", "completed")
        self.assertEqual(self.project_assistant.tasks[0][1].status, "completed")

    def test_add_task_variable(self):
        self.project_assistant.add_task("task1", "description1")
        self.project_assistant.add_task_variable("task1", "variable1", "value1")
        self.assertEqual(
            self.project_assistant.task_variables["task1"]["variable1"], "value1"
        )

    def test_get_task_variables(self):
        self.project_assistant.add_task("task1", "description1")
        self.project_assistant.add_task_variable("task1", "variable1", "value1")
        variables = self.project_assistant.get_task_variables("task1")
        self.assertEqual(variables["variable1"], "value1")

    def test_execute_task(self):
        self.project_assistant.add_task("task1", "description1")
        result = self.project_assistant.execute_task("task1", lambda: "result")
        self.assertEqual(result, "result")

    def test_read_documentation(self):
        docs = self.project_assistant.read_documentation(".")
        self.assertIsInstance(docs, list)

    def test_fill_template_and_add_task(self):
        self.project_assistant.fill_template_and_add_task(
            "task1", "description ${variable}", {"variable": "value"}
        )
        self.assertIn("task1", self.project_assistant.task_variables)

    def test_execute_tasks_based_on_dependencies(self):
        self.project_assistant.add_task("task1", "description1")
        self.project_assistant.add_task(
            "task2", "description2", dependencies=[self.project_assistant.tasks[0][1]]
        )
        self.project_assistant.execute_tasks_based_on_dependencies()
        self.assertEqual(len(self.project_assistant.tasks), 0)


if __name__ == "__main__":
    unittest.main()
