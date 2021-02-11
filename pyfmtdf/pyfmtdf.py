from pyfmtdf.pyfmtdf_formatter import formatter
from pyfmtdf.pyfmtdf_palette import palette
from pyfmtdf.pyfmtdf_parser import parser

class pyfmtdf(object):
    def __init__(self):
        pass

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
