#!/usr/bin/env python3

import sys

from formatter import formatter
from palette import palette
from parser import parser
from checker import checker

def doformat(f):
    fmt = formatter(palette)
    prs = parser(f)
    buf = fmt.start()
    while True:
        item, etype, bold = prs.get_next()
        if item == "":
            break
        buf = "{}{}".format(buf, fmt.format(item, etype, bold))
    buf = "{}{}".format(buf, fmt.end())
    return buf

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: program <script>")
        sys.exit(1)

    tmp = doformat(sys.argv[1])
    if checker.check(sys.argv[1], tmp):
        print(tmp, end="")
    else:
        print("ERROR: Something went wrong")
