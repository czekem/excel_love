import os 
import glob
import csv
import json
import re

import sys
import pathlib
from pathlib import Path



from matplotlib import figure
import pandas as pd
 
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.io as pio


import click
import openpyxl
import inquirer

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def list_of_files():
    pattern = re.compile(r'(check|check if file exist|check for file|list)$')
    question = input('Do you want to check if file exist, or list of all files with nammed extension? Type "check" for file or "list" for list: ').lower()
    result = pattern.match(question)
    try:
        if result:
            return result.group()
    except KeyError:
        sys.exit('No such option to choose. Please try again.')
    else:
        sys.exit('No such option to choose. Please try again.') 

def file_checker():
    filename = input('Please write the name of file: ').lower()
    if '.' in filename:
        name, extension = filename.rsplit('.', maxsplit=1)
        filename = name
    extension = ''
    question = [inquirer.List('question',
                              message='Please choose file extension',
                              choices=['csv', 'xlsx', 'json'])]
    answers = inquirer.prompt(question)
    if answers['question'] == 'csv':
        extension = '.csv'
    if answers['question'] == 'xlsx':
        extension = '.xlsx'
    if answers['question'] == 'json':
        extension = '.json'
    try:
        total = glob.glob(f'{filename}{extension}')
        if not total:
            raise FileNotFoundError
    except FileNotFoundError:
        print("""File not found, please try again and check the name of looked file.""")
        question = input('Do you want to check if file exist, in other folders [Y/N]? '
                         ).lower()
        if question in ['y', 'yes']:
            opening_file = False
            for root, dirs, files in os.walk('/'):
                if filename + extension in files:
                    print(f'The file {filename}{extension} exists in the folder {root}') 
                    question = input('Do you want to open this file? [Y/N]'
                                     ).lower()
                    if question in ['y', 'yes']:
                        full_path = os.path.join(root, filename + extension)
                        list_new = [full_path]
                        if extension == '.xlsx':
                            open_a_file(list_new)
                            opening_file = True
                            break
                        elif extension == '.csv':
                            open_a_file(list_new)
                            opening_file = True
                            break
                        elif extension == '.json':
                            open_a_file(list_new)
                            opening_file = True
                            break
                
            if not opening_file:
                print('File not found')
                
    else:
        print(f'The file {total} exists.')
        question = input('Do you want to read data from this file? [Y/N]'
                         ).lower()
        if question == 'y':
            total = filename + extension
            list_new = [total]
            open_a_file(list_new)


def list_of_extension():
    question = [inquirer.List('question',
                              message='Please choose file extension',
                              choices=['csv', 'xlsx', 'json'])]
    answers = inquirer.prompt(question)
    if answers['question'] == 'csv':
        extension = '*.csv'
    if answers['question'] == 'xlsx':
        extension = '*.xlsx'
    if answers['question'] == 'json':
        extension = '*.json'
    
    new = glob.glob('/*/**/' + extension, recursive=True)
    all = enumerate(new)
    for file in all:
        print(file)
    # new = glob.glob(extension)
    # print(new)
    question = input('Do you want to open this file? [Y/N]').lower()
    if question in ['y' or 'yes']:
        question = input('Please enter write the numer of file position in the list:')
        print([new[int(question)]])
        open_a_file([new[int(question)]])
        
        # open_a_file(new[int(question) - 1])
    



def prepare_question():
    first = [inquirer.List('first_question', 
                           message='Which file you want to open?',
                           choices=['csv', 'xlsx', 'json'])]
        
    answers = inquirer.prompt(first)
    
    if answers['first_question'] == 'csv':
        return 'csv'
    elif answers['first_question'] == 'xlsx':
        return 'xlsx'
    elif answers['first_question'] == 'json':
        return 'json'

def looking_file(first_question):
    name = input('What is the name of the file, without extension? ')
    try: 
        looking_for_file = glob.glob(name + first_question)
        
    except FileNotFoundError:  
        print('File not found')
    
    
    return looking_for_file
            
    
def open_a_file(looking_for_document):
    if looking_for_document: 
        first_file = looking_for_document[0]  
        name, extension = first_file.rsplit('.', maxsplit=1)
        if extension == 'xlsx':
            df = pd.read_excel(first_file, engine='openpyxl')  
            working_on_files(df)
        elif extension == 'csv':
            df = pd.read_csv(first_file)     # try to make code in a "DRY" way
            working_on_files(df)
        elif extension == 'json':
            df = pd.read_json(first_file)
            working_on_files(df)
        else:
            print("Unsupported file extension.")
            return None
    else:
        print("No files found.")
        return None
        ## value error raise zrobić tutaj, albo try and except

def working_on_files(df):
    
    name = input('Please enter the name under which you want to save a file: ') 
    if os.path.exists(name + '.xlsx' or name + '.csv' or name + '.json'):
        print('File already exists')
        question =[inquirer.List('file', message='Do you want to overwrite it?',
                                 choices=['yes', 'no'])]
        answers = inquirer.prompt(question)
        if answers['file'] == 'yes':
            name = name
        if answers['file'] == 'no': 
            question = [inquirer.List('file', message='Do you want to save it under a different name?',
                                      choices=['yes', 'no'])]
            answers = inquirer.prompt(question)
            if answers['file'] == 'yes':
                name = input('Please enter the name under which you want to save a file: ')
            if answers['file'] == 'no':
                print('Operation aborted')
                sys.exit()
                
    pd.set_option('display.max_columns', None)
    print(df.head())    
    df.set_index([col for col in df.columns], inplace=True)
    df = df.reset_index()
    print(df.columns)
    
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
                    max_length = max((len(str(cell)) for cell in column),
                                    default=max_length)
                    adjusted_width = (max_length + 1
                                    ) * 2  
                    worksheet.column_dimensions[get_column_letter(idx+1)
                                                ].width = adjusted_width
        
        if answers['file'] == 'csv':
            
            df.to_csv(name + '.csv', index=False)
       
        if answers['file'] == 'json':
            
            df.to_json(name + '.json', orient='records')
            
    
    except KeyError or AttributeError:
        print('Column not found')
        sys.exit()
                        
    print(f'The file {name}.{answers["file"]} has been saved') 
    
    question = input('Do you want to create a chart from that file? [Y/N] ').lower()
    if question == 'y':
        make_a_chart(df)
        
        
def make_a_chart(data_file):
    # file = data_file
    pd.set_option('display.max_columns', None)
    print(data_file.head()) 
    for_x_axis = input('Please wrote the name of column you want to use as x axis: ')
    for_y_axis = input('Please wrote the name of column you want to use as y axis: ')
    fig = px.scatter(data_file, x=for_x_axis, y=for_y_axis)                                           

    
    folder_path = input("Please enter the folder path where you want to save the chart: ")
    html_file_path = Path(folder_path) / "chart.html"
    png_file_path = Path(folder_path) / "charts.png"
    fig.show()
    
    if not html_file_path.parent.exists():
        html_file_path.parent.mkdir(parents=True)
        print(f" {html_file_path.parent} was created in the tool folder.")
    if not html_file_path.parent.is_dir():
        print(f"{html_file_path.parent} is not a directory.")
        return
    
    fig.write_html(html_file_path)
    html_to_png(html_file_path, png_file_path)



def get_default_save_location():
    if os.name == 'nt': # Windows
        return os.path.join(os.path.expanduser('~'), 'Documents')
    elif os.name == 'posix': 
        return os.path.expanduser('~')
    else:
        return os.path.expanduser('~') 






def html_to_png(html_file_path, png_file_path):
    html_file_path = str(html_file_path)
    png_file_path = str(png_file_path)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920,1080")


    driver = webdriver.Chrome(options=chrome_options)


    driver.get("file://" + html_file_path)

    driver.implicitly_wait(10) 

    driver.save_screenshot(png_file_path)

    driver.quit()








@click.group()
def cli():
    pass
    
@cli.command()
def list_reading():
    """Allow to check if file exist from which User want to obtain data 
    to work on them, or list of all files with nammed extension"""
    first = list_of_files()
    if first == 'check' or first == 'check if file exist' or first == 'check for file':
        file_checker()
    elif first == 'list':
        list_of_extension()
        

 

@cli.command()
def main():

    name_of_file = input('What is the name of the file, without extension? ')
    list_of_files = glob.glob(name_of_file +'.xlsx')
    print(list_of_files)
    first_question = prepare_question()
    looking_for_document = looking_file(first_question)
    openin_a_file = open_a_file(looking_for_document)
    
    

if __name__ == '__main__':
    cli()
    
    





