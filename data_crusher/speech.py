from dataclasses import dataclass
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
import numpy as np

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension
import plotly.graph_objects as go

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import click
import pyttsx3
import tkinter as tk

engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()



@dataclass
class WorkFile:
    def __init__(self, name, extension, df):
        self.name = name
        self.extension = extension
        self.df = df

    def open_file(self):
        file_path = f'{self.name}.{self.extension}'
        try:
            file_search = glob.glob(file_path)
            if not file_search:
                message = 'File not found in the current directory. Searching the entire system...'
                engine.say(message)
                engine.runAndWait()
                raise Exception(message)
            return file_path
        except Exception as e:
            print(e)
            return self.looking_for_file()

    def looking_for_file(self, max_attempts=3):
        name = f'{self.name}.{self.extension}'
        found_files = []
        current_directory_checked = False
        attempts = 0

        while attempts < max_attempts:
            for root, _, files in os.walk('.'):
                if name in files:
                    message = f'The file {name} exists in the folder {root}'
                    print(message)
                    engine.say(message)
                    engine.runAndWait()   # if current_directory_checked else engine.runAndWait()
                    found_files.append(os.path.join(root, name))
                    current_directory_checked = True
                    break  # Break the loop as we found the file

            if not found_files and not current_directory_checked:
                print("File not found in the current directory. Searching the entire system...")
                for root, _, files in os.walk('/'):
                    if name in files:
                        print(f'The file {name} exists in the folder {root}')
                        found_files.append(os.path.join(root, name))
                        break  # Break the loop as we found the file

            attempts += 1

        if len(found_files) > 1:
            print("Multiple files found. Please select one:")
            for i, file_path in enumerate(found_files, start=1):
                print(f"{i}. {file_path}")
            selection = input('Please enter the number of the file you want to open: ')
            return found_files[int(selection) - 1]
        elif len(found_files) == 1:
            return found_files[0]  # Return the first file if only one is found
        else:
            print(f'File {name} not found in the system after {max_attempts} attempts. Exiting the program.')
            sys.exit()



    def read_excel_file(self):
        file_path = self.open_file()
        if self.extension == 'xlsx':
            print("Available worksheets:")
            with pd.ExcelFile(file_path) as xls:
                for sheet in xls.sheet_names:
                    print(sheet)
            sheet_name = input("Please enter the name of the worksheet you want to use: ")
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
            return df
        else:
            pass

    def open_the_file(self):
        pass

    def close_the_file(self):
        pass

class OpenFile(WorkFile):
    def __init__(self, df):
        self.df = df

    def open_the_file(self):
        pd.set_option('display.max_columns', None)
        print(self.df.head())
        headers = self.df.head().to_string(index=False)
        columns = self.df.columns.to_string()
        self.df = self.df.fillna(0.0)
        self.df.set_index([col for col in self.df.columns], inplace=True)
        self.df = self.df.reset_index()
        print(self.df.columns)
        speak('Headers of the DataFrame:')
        speak(headers)
        speak('Columns of the DataFrame:')
        speak(columns)
        headers = []
        while True:
            question = input('Please write the name of the column(s) you want to transfer to another file( please separate it by the commma) and press Enter: ')
            speak(question)
            selected_headers = question.split(',')

            for header in selected_headers:
                if header.strip() in self.df.head():
                    headers.append(header.strip())
                else:
                    print(f'Column {header} not found')
                    sys.exit()

            print('Selected headers:', headers)
            contiune_question = input('Would you like to add another value? (y/n): ')
            if contiune_question != "y":
                break

        possibilities = ['xlsx', 'csv', 'json', 'ods', 'txt', 'html', 'sql']
        name_of_file = input('Please write the name under which you want to save the file:\n').lower()
        name = name_of_file
        question = input("Please write under which extension you want to save the file. 'xlsx', 'csv', 'json', 'ods', 'txt', 'html', 'sql'?: \n").lower()
        if question in possibilities:
            answer = question
        self.df = self.df.loc[:, headers]

        try:
            if answer == 'xlsx':
                with pd.ExcelWriter(name + '.xlsx', engine = 'openpyxl') as writer:
                    self.df.to_excel(writer, sheet_name='Sheet1', index = False)
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']

                    for idx, col in enumerate(self.df.columns):
                        max_length = 6
                        column = self.df[col]
                        max_length = max((len(str(cell)) for cell in column), default=max_length)
                        adjusted_width = (max_length +  3) *  2
                        worksheet.column_dimensions[get_column_letter(idx+1)].width = adjusted_width
                    print('File has been saved')

            if answer == "csv":
                self.df.to_csv(name + '.csv', index=False)
            if answer == 'json':
                self.df.to_json(name + '.json', orient='records')
            if answer == 'ods':
                self.df.to_ods(name + '.ods', index=False)
            if answer == 'txt':
                self.df.to_txt(name + '.txt', index=False)
            if answer == 'html':
                self.df.to_html(name + '.html', index=False)
            if answer == 'sql':
                self.df.to_sql(name + '.sql', index=False)
        except KeyError or AttributeError:
            print('Column not found')
            sys.exit()

        print(f"File {name}.{answer} has been saved")

        question = input("Would you like to make a chart using this data (y/n)? :\n ").lower()
        if question == 'y':
            ChartMaking(self.df).chart()

class ChartMaking(OpenFile):
    def __init__(self, df):
        self.df = df

    def hover_data(self):
        print(self.df.head())
        print(self.df.columns)
        hover_data = []
        while True:
            question = input('Please write the name of the column(s) you want to add as hover data (separate by comma): ')
            selected_hover = question.split(',')

            for header in selected_hover:
                if header.strip() in self.df.columns:
                    hover_data.append(header.strip())
                else:
                    print(f"'{header.strip()}' is not in columns")
                    break

            print('Selected hover_data:', selected_hover)
            continue_question = input('Do you want to add another value? (y/n): ')
            if continue_question != 'y':
                break
        return hover_data

    def chart(self):
        print(self.df.head())
        print(self.df.columns)
        for_x_axis = input('Please write the name of column you want to use as x axis: ')
        for_y_axis = input('Please write the name of column you want to use as y axis: ')

        question = input('Do you want to use a hover data? [Y/N] ').lower()
        if question in ['y', 'yes']:
            hover_data = self.hover_data()
        else:
            hover_data = None

        question = input('What type of chart you want to prepare? [bar, line, scatter, pie, heatmap, violin] ').lower()
        if question == 'scatter':
            fig = px.scatter(self.df, x=for_x_axis, y=for_y_axis, hover_data=hover_data)
        elif question == "bar":
            fig = px.bar(self.df, x=for_x_axis, y=for_y_axis, hover_data=hover_data)
        elif question == "line":
            fig = px.line(self.df, x=for_x_axis, y=for_y_axis, hover_data=hover_data)
        elif question == "pie":
            fig = px.pie(self.df, names=for_x_axis, values=for_y_axis, title='Pie Chart')
        elif question == "heatmap":
            value_column = input('Please write the name of the column you want to aggregate for the heatmap: ')
            fig = px.imshow(self.df.pivot_table(index=for_x_axis, columns=for_y_axis, values=value_column, aggfunc='count'))
        elif question == "violin":
            fig = px.violin(self.df, y=for_y_axis, x=for_x_axis, box=True, hover_data=hover_data)
        else:
            print("No such chart, please try again")
            return

        try:
            fig.show()
        except Exception as e:
            print(f"Error displaying chart: {e}")

def start_question(attempts=3):
    if attempts <= 0:
        print('You have run out of attempts. Please try again later.')
        sys.exit()
        
        
        
        
        
    main_file = input('please write the name of the file and extension. Example: file.csv: ').lower()
    if '.' in main_file:
        name, extension = main_file.rsplit('.', maxsplit=1)
        return name, extension
    else:
        print('Please write the name of file and extension once more')
        return start_question(attempts - 1)







@click.group()
def cli():
    pass

@cli.command()
def file_opening():
    name, extension = start_question()
    work_file = WorkFile(name, extension, df=None)
    file_path = work_file.open_file()
    if file_path:
        df = read_file_based_on_extension(file_path, extension)
        open_file = OpenFile(df)
        open_file.open_the_file()
    else:
        click.echo("File not found or search aborted.")
    
def read_file_based_on_extension(file_path, extension):
    """Read a file based on its extension and return a DataFrame."""
    if extension == 'xlsx':
        df = pd.read_excel(file_path, engine='openpyxl')
    elif extension == 'csv':
        df = pd.read_csv(file_path) # Adjusted delimiter for CSV files
    elif extension == "json":
        df = pd.read_json(file_path)
    elif extension == 'ods':
        df = pd.read_excel(file_path, engine='odf') # Assuming ODS files can be read with the 'odf' engine
    elif extension == 'txt':
        df = pd.read_text(file_path, errors=None)
    elif extension == 'html':
        df = pd.read_html(file_path)[0]
    elif extension == 'sql':
        click.echo("Reading SQL files directly is not supported. Please connect to a database.")
        return None
    else:
        click.echo("Unsupported file extension.")
        return None
    return df


@cli.command()
def chart():
    name, extension = start_question()
    work_file = WorkFile(name, extension, df=None)
    file_path = work_file.open_file()
    df = read_file_based_on_extension(file_path, extension)
    open_file = ChartMaking(df)
    open_file.chart()

    


if __name__ == "__main__":
    cli()
