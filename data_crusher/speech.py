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
