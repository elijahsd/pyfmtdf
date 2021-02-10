import codecs

"""
    "comment": "rgb(150, 150, 150)",
    "string": "rgb(150, 200, 100)",
    "function": "rgb(50, 50, 200)",
    "reserved": "rgb(180, 180, 50)",
    "operator": "rgb(200, 180, 100)",
    "call": "rgb(100, 100, 220)",
    "bracket": "rgb(200, 180, 100)",
    "number": "rgb(200, 50, 50)",
"""

DELIMS = [" ", "\t", "\n", "", "#", "\"", "\'"]

RESERVED = [
    "pass",
    "break",
    "continue",
    "global",
    "nonlocal",
    "assert",
    "del",
    "import",
    "from",
    "as",
    "if",
    "elif",
    "else",
    "while",
    "for",
    "in",
    "with",
    "try",
    "except",
    "finally",
    "return",
    "raise",
    "def",
    "class",
    "lambda",
    "or",
    "and",
    "not",
    "yield",
]

F = ["def", "class"]

VALUES = ["True", "False", "None"]

OPS = "=+-*@/%&|^<>:!"

BRACKETS="[]{}()"

NUMBERS = "0123456789"

class parser(object):
    def __init__(self, text):
        self.position = 0
        self.comment = False
        self.new_line = True
        self.opening = "\""
        self.fname = False

        self.parsers = [
            "parse_br",         # line breaks
            "parse_space",      # spaces
            "parse_comment",    # comments
            "parse_string",     # strings 
            "parse_number",     # numbers 
            "parse_bracket",    # brackets 
            "parse_operator",   # operators
            "parse_text",       # text 
        ]

        with open(text, 'r') as content_file:
            self.text = content_file.read()

    def get_symbol(self):
        if len(self.text) <= self.position:
            return ""
        self.position = self.position + 1
        return self.text[self.position - 1]

    def push_back(self):
        if len(self.text) > self.position:
            self.position = self.position - 1

    def parse_br(self):
        sym = self.get_symbol()
        if sym == '\n':
            self.new_line = True
            return True, "<br>", "none", False
        self.push_back()
        return False, "", "", False

    def parse_space(self):
        sp = "&nbsp;"
        if not self.new_line:
            sp = " "
        self.new_line = False
        sym = self.get_symbol()
        buf = ""
        while sym == ' ' or sym == '\t':
            if sym == ' ':
                buf = "{}{}".format(buf, sp)
            else:
                buf = "{}{}{}{}{}".format(buf, sp, sp, sp, sp)
            sym = self.get_symbol()
        self.push_back()
        if len(buf) > 0:
            return True, buf, "none", False
        return False, "", "", False

    def parse_comment(self):
        sym = self.get_symbol()
        buf = ""
        if sym != "#":
            self.push_back()
            return False, "", "", False
        while sym != '\n' or sym == '':
            buf = "{}{}".format(buf, sym)
            sym = self.get_symbol()
        self.push_back()
        return True, buf, "comment", False

    def triple_seq(self, sym):
        return len(self.text) > (self.position + 2) and self.text[self.position] == sym and self.text[self.position + 1] == sym

    def parse_string(self):
        sym = self.get_symbol()
        buf = ""
        if not self.comment and sym != "\"" and sym != "\'":
            self.push_back()
            return False, "", "", False

        if sym == "":
            return False, "", "", False

        if not self.comment:
            self.opening = sym
            if self.triple_seq(sym):
                buf = "{}{}".format(sym, sym)
                self.position = self.position + 2
                self.comment = True
            buf = "{}{}".format(buf, sym)
        else:
            self.push_back()

        esc = False
        while True:
            sym = self.get_symbol()
            if sym == "":
                break
            if not self.comment:
                if sym == self.opening and not esc:
                    buf = "{}{}".format(buf, sym)
                    return True, buf, "string", False
            else:
                if sym == "\n":
                    self.push_back()
                    return True, buf, "string", False
                if sym == self.opening and not esc and self.triple_seq(sym):
                    buf = "{}{}{}{}".format(buf,sym, sym, sym)
                    self.position = self.position + 2
                    self.comment = False
                    return True, buf, "string", False
            buf = "{}{}".format(buf, sym)
            if esc:
                esc = False
            elif sym == "\\":
                esc = True

        return False, "", "", False

    def parse_symbols(self, symbols, ent):
        sym = self.get_symbol()
        buf = ""
        while sym != "" and sym in symbols:
            buf = "{}{}".format(buf, sym)
            sym = self.get_symbol()
        self.push_back()
        if len(buf) > 0:
            return True, buf, ent, False
        return False, "", "", False

    def parse_number(self):
        return self.parse_symbols(NUMBERS, "number")

    def parse_bracket(self):
        return self.parse_symbols(BRACKETS, "bracket")

    def parse_operator(self):
        return self.parse_symbols(OPS, "operator")

    def parse_text(self):
        sym = self.get_symbol()
        buf = ""
        spec = ".,_"
        func = self.fname
        self.fname = False
        while sym != "" and (sym.isalpha() or (sym in NUMBERS) or (sym in spec)):
            buf = "{}{}".format(buf, sym)
            sym = self.get_symbol()
        self.push_back()
        if len(buf) > 0:
            self.fname = buf in F
            return True, buf, buf in RESERVED and "reserved" or (func or buf in VALUES) and "function" or "none", func
        return False, "", "", False

    def get_next(self):
        for f in self.parsers:
            res, t, e, b = getattr(self, f)()
            if res:
                return t, e, b

        return "", "", False
