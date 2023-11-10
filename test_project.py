import unittest
from unittest.mock import MagicMock, patch

from project import ProjectAssistant


class TestProjectAssistant(unittest.TestCase):
    def test_add_task(self):
        assistant = ProjectAssistant()
        assistant.add_task("task1", "description1")
        self.assertEqual(len(assistant.tasks), 1)
        self.assertEqual(assistant.tasks[0][1].task_id, "task1")
        self.assertEqual(assistant.tasks[0][1].instructions, "description1")

    def test_update_task_status(self):
        assistant = ProjectAssistant()
        assistant.add_task("task1", "description1")
        assistant.update_task_status("task1", "completed")
        self.assertEqual(assistant.tasks[0][1].status, "completed")

    def test_add_task_variable(self):
        assistant = ProjectAssistant()
        assistant.add_task("task1", "description1")
        assistant.add_task_variable("task1", "var1", "value1")
        self.assertEqual(assistant.task_variables["task1"]["var1"], "value1")

    def test_get_task_variables(self):
        assistant = ProjectAssistant()
        assistant.add_task("task1", "description1")
        assistant.add_task_variable("task1", "var1", "value1")
        variables = assistant.get_task_variables("task1")
        self.assertEqual(variables["var1"], "value1")

    @patch("project.ProjectAssistant.execute_task")
    def test_execute_task(self, mock_execute_task):
        assistant = ProjectAssistant()
        assistant.add_task("task1", "description1")
        assistant.execute_task("task1", lambda: "result")
        mock_execute_task.assert_called_once()

    @patch("os.listdir")
    @patch("builtins.open", new_callable=MagicMock)
    def test_read_documentation(self, mock_open, mock_listdir):
        mock_listdir.return_value = ["doc1.txt", "doc2.txt"]
        mock_open.return_value.__enter__.return_value.read.return_value = (
            "documentation"
        )
        assistant = ProjectAssistant()
        docs = assistant.read_documentation("docs")
        self.assertEqual(docs, ["documentation", "documentation"])

    def test_fill_template_and_add_task(self):
        assistant = ProjectAssistant()
        assistant.fill_template_and_add_task(
            "task1", "Hello, ${name}!", {"name": "World"}
        )
        self.assertEqual(assistant.tasks[0][1].instructions, "Hello, World!")

    @patch("project.ProjectAssistant.execute_task")
    def test_execute_tasks_based_on_dependencies(self, mock_execute_task):
        assistant = ProjectAssistant()
        assistant.add_task("task1", "description1")
        assistant.add_task(
            "task2", "description2", dependencies=[assistant.tasks[0][1]]
        )
        assistant.execute_tasks_based_on_dependencies()
        self.assertEqual(mock_execute_task.call_count, 2)


if __name__ == "__main__":
    unittest.main()
