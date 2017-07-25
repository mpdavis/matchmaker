
import ast
import json


def load_file(file_path):
    """
    Helper for loading data out of a file
    
    Attempts to load json or a python literal.
    """
    
    try:
        return _load_json(file_path)
    except ValueError:
        pass
    
    return _load_python_literal(file_path)


def _load_json(file_path):
    """
    Load a json file into memory.
    """
    with open(file_path) as file_data:
        data = json.load(file_data)
    
    return data


def _load_python_literal(file_path):
    """
    Load a python literal into memory.
    
    As provided, the sample data is not strictly json but a python literal
    written to a file.
    """
    
    with open(file_path) as file_data:
        data = ast.literal_eval(file_data.read())
        
    return data
