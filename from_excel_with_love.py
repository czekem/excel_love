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



def open_a_file(looking_for_document):
    if looking_for_document:  # Check if the list is not empty
        first_file = looking_for_document[0]  # Take the first file from the list
        name, extension = first_file.rsplit('.', maxsplit=1)
        if extension == 'xlsx':
            df = pd.read_excel(first_file, engine='openpyxl')  # Use the first_file variable
            working_on_files(df)
        else:
            print("Unsupported file extension.")
            return None
    else:
        print("No files found.")
        return None


def working_on_files(df):
        
    df.set_index([col for col in df.columns], inplace=True)
    df = df.reset_index()
    df = df.loc[:, ['Numer spedycji', 'Numer Zlecenia', 'Zysk',]]

    with  pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        for idx, col in enumerate(df.columns):
            max_length = 6
            column = df[col]
            max_length = max((len(str(cell)) for cell in column), default=max_length)
            adjusted_width = (max_length +  1) *  1 # < - Here I can really make the  cells "wider" by much, just to change '1' to other value
            worksheet.column_dimensions[get_column_letter(idx+1)].width = adjusted_width
   
            
        print(f'The file output.xlsx has been saved')
