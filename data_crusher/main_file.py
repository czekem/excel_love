from dataclasses import dataclass
from standart import *
import os 
import glob
import csv
import json
import re
from speech import *
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


engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def display_text_larger(text):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    label = tk.Label(root, text=text, font=("Helvetica", 24))
    label.pack()
    root.mainloop()


def main():
    message = 'Hello to the Data Crusher, We want you to help working with xlsx file, odts file, csv file or json file, as smooth as possible'
    engine.say(message)
    engine.runAndWait()
    print(message)
    main_question = 'Please choose if you want messages to be spoken, written using bigger font or standard? Please type bigger, spoken or nothing.\n'
    engine.say(main_question)
    engine.runAndWait()
    important_question = input(main_question).lower()
    try:
        if important_question in ['bigger', 'big']:
            print('Work in progress')
        elif important_question in ["spoken", "speaking", "speak"]:
            pass
        elif important_question in ['nothing', 'n', 'nothi']:
            file = input('Please enter the name of the file: ')
            if '.' in file:
                file = file.split(".")[0]
            extension = input('Please enter the extension of the file: ').lower()
            if '.' in extension:
                extension = extension.split(".")[0]
            if extension in ['csv', 'json', 'xlsx', 'ods', 'txt', 'html', 'sql']:
                extension = extension
            elif '.' not in extension:
                extension = extension
                
            else:
                print('Unsupported file extension.')
                question = input('Do you want to start again? [Y/N]').lower()
                if question in ['y', 'yes']:
                    main()
                else:
                    message = 'The program was closed.'
                    sys.exit(message)
            print(file, extension)
            work_file = WorkFile(file, extension, df=None)
            file_path = work_file.open_file()
            if file_path:
                df = work_file.read_excel_file()
                open_file = OpenFile(df=df)
                open_file.open_the_file()
            else:
                click.echo("File not found or search aborted.")
    except KeyboardInterrupt:
        message = 'Program has suddenly terminated. Please start again.'
        engine.say(message)
        engine.runAndWait()
        print(message)
        sys.exit()

    
    
    

if __name__ == "__main__":
    main()
