import codecs

class Parser(object):
    def __init__(self, text, rules):
        self.position = 0
        self.comment = False
        self.new_line = True
        self.opening = "\""
        self.fname = False
        self.rules = rules

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
        if len(self.text) == self.position:
            return ""
        self.position = self.position + 1
        return self.text[self.position - 1]

    def push_back(self, sym):
        if sym != "":
            self.position = self.position - 1

    def parse_br(self):
        sym = self.get_symbol()
        if sym == "\n":
            self.new_line = True
            return True, "<br>", "none", False
        self.push_back(sym)
        return False, "", "", False

    def parse_space(self):
        sp = "&nbsp;"
        if not self.new_line:
            sp = " "
        self.new_line = False
        sym = self.get_symbol()
        buf = ""
        while sym == " " or sym == "\t":
            if sym == " ":
                buf = "{}{}".format(buf, sp)
            else:
                buf = "{}{}{}{}{}".format(buf, sp, sp, sp, sp)
            sym = self.get_symbol()
        self.push_back(sym)
        if len(buf) > 0:
            return True, buf, "none", False
        return False, "", "", False

    def parse_comment(self):
        sym = self.get_symbol()
        buf = ""
        # TODO: use multiple symbols, i.e. "//"
        # TODO: multiline comment, i.e. "/* */" or '""" """' or "''' '''"
        if sym != self.rules.one_line_comment:
            self.push_back(sym)
            return False, "", "", False
        while sym != "\n" and sym != "":
            buf = "{}{}".format(buf, sym)
            sym = self.get_symbol()
        self.push_back(sym)
        return True, buf, "comment", False

    # TODO: remove
    def triple_seq(self, sym):
        return len(self.text) > (self.position + 2) and self.text[self.position] == sym and self.text[self.position + 1] == sym

    def parse_string(self):
        sym = self.get_symbol()
        buf = ""
        if not self.comment and sym != "\"" and sym != "\'":
            self.push_back(sym)
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
            self.push_back(sym)

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
                # TODO: create special rule
                if sym == "\n":
                    self.push_back(sym)
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
        self.push_back(sym)
        if len(buf) > 0:
            return True, buf, ent, False
        return False, "", "", False

    def parse_number(self):
        return self.parse_symbols(self.rules.numbers, "number")

    def parse_bracket(self):
        return self.parse_symbols(self.rules.brackets, "bracket")

    def parse_operator(self):
        return self.parse_symbols(self.rules.ops, "operator")

    def bracket_follow(self):
        forw = 0
        found = False
        while True:
            sym = self.get_symbol()
            if sym == "":
                return False
            forw = forw + 1
            if sym in self.rules.spaces:
                continue
            if sym == "(":
                found = True
            break
        self.position = self.position - forw
        return found

    def parse_text(self):
        sym = self.get_symbol()
        buf = ""
        func = self.fname
        self.fname = False
        while sym != "" and (sym.isalpha() or (sym in self.rules.numbers) or (sym in self.rules.treated_as_text)):
            buf = "{}{}".format(buf, sym)
            sym = self.get_symbol()
            # TODO: use multisymbol, i.e. "->"
            if sym in self.rules.fields:
                buf = "{}{}".format(buf, sym)
                sym = self.get_symbol()
                break
        self.push_back(sym)
        if len(buf) > 0:
            self.fname = buf in self.rules.f
            return True, buf, (buf in self.rules.reserved) and "reserved" or (func or (buf in self.rules.values)) and "function" or ((buf[0].isalpha() or (buf[0] == "_")) and self.bracket_follow()) and "call" or "none", func
        return False, "", "", False

    def get_next(self):
        for f in self.parsers:
            res, t, e, b = getattr(self, f)()
            if res:
                return t, e, b

        return "", "", False
