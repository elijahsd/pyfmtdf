#!/usr/bin/env python3

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

    p = DEFAULT_PALETTE
    r = DEFAULT_RULES

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
