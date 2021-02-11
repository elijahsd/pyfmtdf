# pyfmtdf

## Description

This program accepts the python file on input and formats it into HTML on output.  
pyfmtdf stands for "PYthon ForMaTter for Discussion Forum".

## Details

This program has been created under MIT license by Illia Ragozin for University of the People with the purpose to make the code posted on the discussion forums more readable.  
  
`Usage: pyfmtdf <script name>`
  
The output is printed to stdout.  
The colors can be changes in palette.py  
  
The program has internal checker which compares the input file with the result of the HTML rendering to ensure a proper conversion. Use `--check` option to enable the checker.

## Installation

1. Download the code from [Github](https://github.com/elijahsd/pyfmtdf "Github").
2. From the directory containing setup.py, run install using PIP: `pip install .`

## Usage

### From command line

To convert your python code into HTML:
1. Run checker first: `python3 -m pyfmtdf --check <script>`.
2. If checker didn't find any problems, convert the code into HTML: `python3 -m pyfmtdf <script>`.
3. Copy the output.

### As a module

It is possible to use import the module into your program:  
`
from pyfmtdf import pyfmtdf

out = pyfmtdf.pyfmtdf.doformat(<path to the script>)
`

## Linux users tips

1. It is useful to copy the output directly to the clipboard: `python3 -m pyfmtdf <script> | xclip`.
2. You can play with colors and immediately see the difference, just use a browser: `python3 -m pyfmtdf <script> | firefox "data:text/html;base64,$(base64 -w 0 <&0)"`.

## Bugs

In case of any bugs, or if the checker fails, feel free to create an issue. You might want to leave your contact information for me to follow up on details.
