import os 
import glob

import pandas as pd
import click
import openpyxl
import inquirer

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension

def list_of_files():
    question = [inquirer.List('question',
                              message="""Do you want to check if file exist,
                              or list of all files with nammed extension?""",
                              choices=['check', 'list'])]
    answers = inquirer.prompt(question)
    if answers['question'] == 'check':
        file_checker()




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
        
        except FileNotFoundError:   # Work on raiseError if user would type xlsx.xlsx or something like that by pure mistake
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
    
 
            if answers['file'] == 'yes':
                name = input('Please enter the name under which you want to save a file: ')
            if answers['file'] == 'no':
                print('Operation aborted')
                sys.exit()
        
    df.set_index([col for col in df.columns], inplace=True)
    df = df.reset_index()
    print(df.columns)
    # question = input('Please write the name of the column you want to transfer to another file: ')  - unecessary now
    headers = []
    while True:
        question = [inquirer.Text('headers', message="Please enter the headers"
                                  )]
        answers = inquirer.prompt(question)
        try:
            if answers['headers'] in df.columns:
                headers.append(answers['headers'])

        except ValueError:
            print("Invalid input, please enter corret header.")
        next_addition = input('Do you want to add another header? (y/n): '
                              ).lower()
        if next_addition != 'y':
            break
    
    question = [inquirer.List('file', message='Under which extensions you want to save the file?',
                              choices=['xlsx', 'csv', 'json'])]
    
    answers = inquirer.prompt(question)
    
    df = df.loc[:, headers]
    
    try:
        if answers['file'] == 'xlsx':
    
            with pd.ExcelWriter(name + '.xlsx', engine='openpyxl') as writer:
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


      
@click.group()
def cli():
    pass
    
@cli.command()
def list_reading():
    first = list_of_files()
 
 

@cli.command()
def main():
    name_of_file = input('What is the name of the file, without extension? ')
    list_of_files = glob.glob(name_of_file +'.xlsx')
    print(list_of_files)
    first_question = prepare_question()
    looking_for_document = looking_file(first_question)
    openin_a_file = open_a_file(looking_for_document)
    # working_on_file = working_on_files(df)
    
    
    
    

if __name__ =='__main__':
    cli()
