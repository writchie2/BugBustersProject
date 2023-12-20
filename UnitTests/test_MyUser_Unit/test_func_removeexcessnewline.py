import sys

from SchedulingApp.Model_Classes.MyUser_Functions import func_RemoveExcessNewLine

sys.path.append('../../SchedulingApp')
from SchedulingApp.Model_Classes.MyUser_Functions import func_RemoveExcessNewLine
from django.test import TestCase

class RemoveExcessNewLineTest(TestCase):
    def setUp(self):
        self.good_strings=[
            "Normal string\r\n",
            "Normal string\r\nWith normal space\r\n"
            "Normal string\r\nwith a newline\r\nthen another.\r\n"
        ]


    def test_NoRemovalNeeded(self):
        for string in self.good_strings:
            self.assertEqual(string, func_RemoveExcessNewLine(string), "Something removed from" + string)

    def test_StringIsFormatted(self):
        result = func_RemoveExcessNewLine("\r\nstarts with a newline\r\n")
        self.assertEqual(result, "starts with a newline\r\n", "starting newline not removed")

        result = func_RemoveExcessNewLine("has no newline at the end")
        self.assertEqual(result, "has no newline at the end\r\n", "did not add newline")

        result = func_RemoveExcessNewLine("has multiple newlines\r\n\r\n")
        self.assertEqual(result, "has multiple newlines\r\n", "did not remove multiple newlines")

        result = func_RemoveExcessNewLine("has excessive newlines\r\n\r\n\r\n\r\n\r\n")
        self.assertEqual(result, "has excessive newlines\r\n", "did not remove excessive newlines")

        result = func_RemoveExcessNewLine("multiple\r\n\r\nnewlines in the middle\r\n")
        self.assertEqual(result, "multiple\r\nnewlines in the middle\r\n", "did not remove middle newlines")