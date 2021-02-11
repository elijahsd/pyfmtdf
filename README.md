# pyfmtdf

## Description

This program accepts the python file on input and formats it into HTML on output.  
pyfmtdf stands for "PYthon ForMaTter for Discussion Forum".

## Details

This program has been created for University of the People with the purpose to make the code posted on the discussion forums more readable.  
`Usage: pyfmtdf <script name>`

The output is printed to stdout.  
The colors can be changes in palette.py  

## Installation

1. Download the code from [Github](https://github.com/elijahsd/pyfmtdf "Github").
2. From the directory containing setup.py, run install using PIP: `pip install .`

## Usage

### From command line

To convert your python code into HTML:
1. Run checker first: `python3 -m pyfmtdf --check <script>`.
2. If checker didn't find any problems, convert the code into HTML: `python3 -m pyfmtdf <script>`.

### As a module

It is possible to use import the module into your program:  
`
from pyfmtdf import pyfmtdf

out = pyfmtdf.pyfmtdf.doformat(<path to the script>)
`
