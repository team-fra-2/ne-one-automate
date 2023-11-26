import base64

# needs imports for rules
from models.one_record import ChangeRequest, Recommendation, Decision
from typing import Optional
from rule_engine.functions import *


# Function to decode and load the function
def load_rule(encoded_function):
    decoded_function = base64.b64decode(encoded_function).decode("utf-8")
    exec(decoded_function, globals())
    return globals()[get_rule_name(decoded_function)]


# Helper function to extract the function name
def get_rule_name(func_code):
    lines = func_code.splitlines()
    for line in lines:
        if line.startswith("def "):
            return line.split("def ")[1].split("(")[0]
    return None
