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

def test_logic_file_open_xlsx():
    file = 'file.xlsx'
    name, extension = file.rsplit('.', maxsplit=1)
    assert extension == 'xlsx'

def tests_file_open_extension_xlsx():
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp:
        temp_file_path = temp.name
        
    name, extension = temp_file_path.rsplit('.', maxsplit=1)
    
    os.remove(temp_file_path)
    assert extension == 'xlsx'

def test_logic_file_open_csv():
    file = 'file.csv'
    name, extension = file.rsplit('.', maxsplit=1)
    assert extension == 'csv'


def test_open_file_extension_csv():
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
        temp_file_path = temp.name
        
    name, extension = temp_file_path.rsplit('.', maxsplit=1)
    
    os.remove(temp_file_path)
    assert extension == 'csv'

    

def test_open_file_extension_json():
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
        temp_file_path = temp.name
        
    name, extension = temp_file_path.rsplit('.', maxsplit=1)
    
    os.remove(temp_file_path)
    assert extension == 'json'


def test_logic_file_open_json():
    file = 'file.json'
    name, extension = file.rsplit('.', maxsplit=1)
    assert extension == 'json'
    

def test_create_a_chart_bar_chart_novice_approach():
    x_axis = ['a', 'b', 'c']
    y_axis = [1, 2, 3]
    plt.bar(x_axis, y_axis)
    plt.xlabel('x_axis')
    plt.ylabel('y_axis')
    assert plt.bar is not None




