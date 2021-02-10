#!/usr/bin/env python3

import sys

from formatter import formatter
from palette import palette
from parser import parser

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: program <script>")
        sys.exit(1)

    fmt = formatter(palette)
    prs = parser(sys.argv[1])
    print(fmt.start(), end="")
    while True:
        item, etype, bold = prs.get_next()
        if item == "":
            break
        print(fmt.format(item, etype, bold), end="")
        #print(fmt.format(item, etype))
    print(fmt.end(), end="")
