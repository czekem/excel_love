# Here will be some test of the tool funcionality, 

from matplotlib import pyplot as plt
from pandas8_6 import list_of_files, looking_file, open_a_file, make_a_chart
import re
import sys
import glob
import os
import tempfile

def test_match_check_pattern():
    pattern = re.compile(r'(check|check if file exist|check for file|list)$')
    question = 'check'
    result = pattern.match(question)
    assert result is not None
    
    
def test_match_list_pattern():
    pattern = re.compile(r'(check|check if file exist|check for file|list)$')
    question = 'list'
    result = pattern.match(question)
    assert result is not None


def test_entering_wrong_option():
    pattern = re.compile(r'(check|check if file exist|check for file|list)$')
    question = 'wrong'
    result = pattern.match(question)
    assert result is None


def test_enter_looking_file():
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
        temp_file_path = temp.name
        
    name = 'alice'
    first_question = '.txt'

    test_enter_looking_file = glob.glob(name + first_question)
    
    os.remove(temp_file_path)

    assert test_enter_looking_file is not None
