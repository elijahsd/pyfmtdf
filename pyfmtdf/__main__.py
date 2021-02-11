#!/usr/bin/env python3

import sys

from pyfmtdf.pyfmtdf import pyfmtdf
from pyfmtdf.pyfmtdf_checker import checker

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: program <script>")
        sys.exit(1)

    tmp = pyfmtdf.doformat(sys.argv[1])
    if checker.check(sys.argv[1], tmp):
        print(tmp, end="")
    else:
        print("ERROR: Something went wrong")
