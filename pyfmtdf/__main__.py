#!/usr/bin/env python3

import sys

from pyfmtdf.pyfmtdf import pyfmtdf
from pyfmtdf.pyfmtdf_checker import checker

def usage():
    print("Usage: program [--check] <script>")
    sys.exit(1)

if __name__ == "__main__":
    check = False
    f = None

    if (len(sys.argv) != 2) and (len(sys.argv) != 3):
        usage()

    if len(sys.argv) == 3:
        if sys.argv[1] != "--check":
            usage()
        else:
            check = True
            f = sys.argv[2]
    else:
        f = sys.argv[1]

    tmp = pyfmtdf.doformat(f)
    if not check:
        print(tmp, end="")
    else:
        if checker.check(f, tmp):
            print("SUCCESS: Looks good!")
        else:
            print("ERROR: Some differences!")
