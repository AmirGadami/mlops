import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail):
        last_trace = traceback.extract_tb(error_detail.__traceback__)[-1]
        file_name = last_trace.filename
        line_number = last_trace.lineno
        return f"Error: {error_message} | File: {file_name} | Line: {line_number}"

    def __str__(self):
        return self.error_message
