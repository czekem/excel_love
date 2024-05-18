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
