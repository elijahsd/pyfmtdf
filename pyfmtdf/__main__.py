#!/usr/bin/env python3

import argparse
import importlib
import sys

from pyfmtdf.pyfmtdf_main import Pyfmtdf
from pyfmtdf.pyfmtdf_checker import Checker

DEFAULT_PALETTE = "default"
DEFAULT_RULES = "python"

def usage():
    print("Usage: program [--check] <script>")
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Script to format")
    parser.add_argument("-c", "--check", help="Check the result for validity", action="store_true")
    parser.add_argument("-r", "--rule", help="Rules name (default: python)")
    parser.add_argument("-p", "--palette", help="Palette name (default: default)")
    args = parser.parse_args()

    check = args.check
    f = args.file

    p = args.palette or DEFAULT_PALETTE
    r = args.rule or DEFAULT_RULES

    palette_mod = importlib.import_module("pyfmtdf.palettes.{}".format(p))
    rules_mod = importlib.import_module("pyfmtdf.rules.{}".format(r))

    fmtr = Pyfmtdf(palette_mod.palette, rules_mod.rules)
    tmp = fmtr.doformat(f)

    if not check:
        print(tmp, end="")
    else:
        if Checker.check(f, tmp):
            print("SUCCESS: Looks good!")
        else:
            print("ERROR: Some differences!")
