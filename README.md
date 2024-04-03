![EasySelect Logo](https://github.com/czekem/excel_love/blob/main/ec777f4a74014805b9f40ca39caedbdd.png)



# EasySelect: Your One-Stop Tool for Managing and Manipulating Data Across File Formats (Excel, CSV, JSON)


EasySelect is a user-friendly Python application designed to simplify data management by allowing you to select, transfer, and summarize columns across common file formats (Excel, CSV, JSON). This tool empowers you to effectively manipulate your data without requiring any programming knowledge. It's made mainly to make working on Excel and other files like CSV or JSON and make an easier interaction between them as transferring the data

from one file to the another.


**Features:**


* Supports various file formats: Excel (.xlsx), CSV, and JSON

* Intuitive interface enables easy selection of desired columns and values

* Generates summaries of chosen columns for quick data analysis

* Saves data modifications to the user-specified file format

* Planned desktop application (GUI) for user-friendly interaction (will be added soon)

* Create a graph using plot library (will be added soon)

* Create a user interference (would be grateful for help here)

* Create a tool in that way, that it would be easy-usable for people with different disabilities

* Added test.py for testing functions that are in the code.


**What the code is doing now already?**


For this moment (30.03.2024) the script can do :


* Open any .xlsx, .JSON or .csv file that would be in the same directory as the script

* Look for named file (with the extension) in whole computer memory, and enum every file, so you could choose it by entering a correct number

* Giving possibility to "extract" the columns with their data from the main file to the file that We want to create

* Save the file as the .xlsx, .JSON or .csv (it will be added in the following days)

* Allowing to create charts right after creating new file and save them in the newly created folder

** Know Problems : **

* Script isn't working best ( for this moment of course), if got more than one worksheet in the excel, or one worksheet with the table and and chart in it.
* Need to add a possibilty for choosing working sheet in "xlsx" file

** Want I want to add : **

* Make script "transfer" to classes, so it will be correct with OOP, and will allow for more flexibility on expanding the code.




MIT License

Copyright (c) 2024 Michał Czekaj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
  
