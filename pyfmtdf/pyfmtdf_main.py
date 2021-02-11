from pyfmtdf.pyfmtdf_formatter import Formatter
from pyfmtdf.pyfmtdf_parser import Parser

class Pyfmtdf(object):
    def __init__(self, palette, rules):
        self.palette = palette
        self.rules = rules

    def doformat(self, f):
        fmt = Formatter(self.palette)
        prs = Parser(f, self.rules)
        buf = fmt.start()
        while True:
            item, etype, bold = prs.get_next()
            if item == "":
               break
            buf = "{}{}".format(buf, fmt.format(item, etype, bold))
        buf = "{}{}".format(buf, fmt.end())
        return buf
