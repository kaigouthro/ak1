import unittest
from unittest.mock import MagicMock, patch

from project import ProjectAssistant, Task


class TestProjectAssistant(unittest.TestCase):
    def setUp(self):
        self.pa = ProjectAssistant()

    def test_add_task(self):
        self.pa.add_task("task1", "description1")
        self.assertEqual(len(self.pa.tasks), 1)
        self.assertEqual(self.pa.tasks[0][1].task_id, "task1")

    def test_update_task_status(self):
        self.pa.add_task("task1", "description1")
        self.pa.update_task_status("task1", "completed")
        self.assertEqual(self.pa.tasks[0][1].status, "completed")

    def test_add_task_variable(self):
        self.pa.add_task("task1", "description1")
        self.pa.add_task_variable("task1", "var1", "value1")
        self.assertEqual(self.pa.task_variables["task1"]["var1"], "value1")

    def test_get_task_variables(self):
        self.pa.add_task("task1", "description1")
        self.pa.add_task_variable("task1", "var1", "value1")
        variables = self.pa.get_task_variables("task1")
        self.assertEqual(variables["var1"], "value1")

    @patch("project.ProjectAssistant.execute_task")
    def test_execute_task(self, mock_execute_task):
        self.pa.add_task("task1", "description1")
        self.pa.execute_task("task1", MagicMock())
        mock_execute_task.assert_called_once()

    @patch("os.listdir")
    @patch("builtins.open", new_callable=MagicMock)
    def test_read_documentation(self, mock_open, mock_listdir):
        mock_listdir.return_value = ["file1"]
        mock_open.return_value.__enter__.return_value.read.return_value = "content1"
        contents = self.pa.read_documentation("path")
        self.assertEqual(contents, ["content1"])

    def test_fill_template_and_add_task(self):
        self.pa.fill_template_and_add_task(
            "task1", "Hello, ${name}!", {"name": "World"}
        )
        self.assertEqual(self.pa.tasks[0][1].instructions, "Hello, World!")

    @patch("project.ProjectAssistant.execute_task")
    def test_execute_tasks_based_on_dependencies(self, mock_execute_task):
        task1 = Task("task1", "description1")
        task2 = Task("task2", "description2", dependencies=[task1])
        self.pa.tasks.append((0, task1))
        self.pa.tasks.append((0, task2))
        self.pa.execute_tasks_based_on_dependencies()
        self.assertEqual(mock_execute_task.call_count, 2)


if __name__ == "__main__":
    unittest.main()
