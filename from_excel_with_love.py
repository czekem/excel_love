import os 
import glob

import pandas as pd
import click
import openpyxl
import inquirer

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension



def prepare_question():
    first = [inquirer.List('first_question', message = 'Which file you want to open?', choices =
                           ['csv','xlsx', 'json'])]
        
    answers = inquirer.prompt(first)
    
    if answers['first_question'] == 'csv':
        return 'csv'
    elif answers['first_question'] == 'xlsx':
        return 'xlsx'
    elif answers['first_question'] == 'json':
        return 'json'

def looking_file(first_question):
    if first_question == 'xlsx':
        name = input('What is the name of the file, without extension? ')
        try: 
            looking_for_file = glob.glob(name + '.xlsx')
        
        except FileNotFoundError:   # tutaj też mogę dać raiseError gdyby ktoś bardo chciał dać np. cow.xlsx.xlsx
            print('File not found')
            
    return looking_for_file
