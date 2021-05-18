class Parser(object):
    def __init__(self, text, rules):
        self.position = 0
        self.comment = None
        self.new_line = True
        self.fname = False
        self.rules = rules
        self.overflow = False

        self.parsers = [
            "parse_br",         # line breaks
            "parse_space",      # spaces
            "parse_comment",    # comments
            "parse_string",     # strings 
            "parse_number",     # numbers 
            "parse_bracket",    # brackets 
            "parse_operator",   # operators
            "parse_field",      # fields
            "parse_text",       # text 
        ]

        with open(text, 'r') as content_file:
            self.text = content_file.read()

    def get_symbols(self, count = 1):
        if len(self.text) == self.position:
            self.overflow = True
            return ""
        if len(self.text) < self.position + count:
            return ""
        self.position = self.position + count
        return self.text[self.position - count:self.position]

    def push_back(self, pos = 1):
        if not self.overflow:
            self.position = self.position - pos

    def parse_br(self):
        sym = self.get_symbols()
        if sym == "\n":
            self.new_line = True
            return True, "<br>", "none"
        self.push_back()
        return False, "", ""

    def parse_space(self):
        sp = "&nbsp;"
        if not self.new_line:
            sp = " "
        # parse_space is called right after parse_br
        # so this is an appropriate place to reset new_line
        # At the beginning we use non-break spaces, and then we are fine
        # to use regular ones and allow the line to break
        self.new_line = False
        sym = self.get_symbols()
        buf = ""
        while sym == " " or sym == "\t":
            if sym == " ":
                buf = "{}{}".format(buf, sp)
            else:
                buf = "{}{}{}{}{}".format(buf, sp, sp, sp, sp)
            sym = self.get_symbols()
        self.push_back()
        if len(buf) > 0:
            return True, buf, "none"
        return False, "", ""

    def parse_comment_single(self, boundaries):
        if self.comment != None:
            if self.comment != boundaries:
                return ""
        start = boundaries[0]
        end = boundaries[1]
        esc = boundaries[2]
        syms = ""
        if self.comment == None:
            syms = self.get_symbols(len(start))
            if syms == "":
                return ""
            if syms != start:
                self.push_back(len(syms))
                return ""
            self.comment = boundaries
        buf = ""
        buf += syms
        sym = self.get_symbols()
        while sym != "":
            if sym == "\n" and end != "\n":
                break
            buf += sym
            sym = self.get_symbols()
            if len(buf) < (len(start) + len(end)):
                continue
            # check for the end of the comment, make sure the leading symbol is not escaped
            escaped = False
            if len(buf) > (len(start) + len(end)):
                pred = buf[-len(end)-1:-len(end)]
                escaped = pred in esc
            if not escaped and buf[-len(end):] == end:
                # special case, eol
                if end == '\n':
                    self.push_back()
                    buf = buf[:-1]
                self.comment = None
                break
        self.push_back()
        return buf

    def parse_comment(self):
        for c in self.rules.comment:
            r = self.parse_comment_single(c)
            if r:
                return True, r, "comment"
        for c in self.rules.comment_string:
            r = self.parse_comment_single(c)
            if r:
                return True, r, "string"
        return False, "", ""

    def parse_string(self):
        for c in self.rules.string:
            r = self.parse_comment_single(c)
            if r:
                return True, r, "string"
        return False, "", ""

    def parse_symbols(self, symbols, ent):
        sym = self.get_symbols()
        buf = ""
        while sym != "" and sym in symbols:
            buf = "{}{}".format(buf, sym)
            sym = self.get_symbols()
        self.push_back()
        if len(buf) > 0:
            return True, buf, ent
        return False, "", ""

    def parse_number(self):
        return self.parse_symbols(self.rules.numbers, "number")

    def parse_bracket(self):
        return self.parse_symbols(self.rules.brackets, "bracket")

    def parse_operator(self):
        return self.parse_symbols(self.rules.ops, "operator")

    def parse_field(self):
        return self.parse_symbols(self.rules.fields, "field")

    def bracket_follow(self):
        forw = 0
        found = False
        while True:
            sym = self.get_symbols()
            if sym == "":
                break
            forw = forw + 1
            if sym in self.rules.spaces:
                continue
            if sym == "(":
                found = True
            break
        self.position = self.position - forw
        return found

    def parse_text(self):
        sym = self.get_symbols()
        buf = ""
        func = self.fname
        self.fname = False
        while sym != "" and (sym in self.rules.text):
            buf = "{}{}".format(buf, sym)
            sym = self.get_symbols()
        self.push_back()
        if len(buf) > 0:
            self.fname = buf in self.rules.f
            t = "none"
            if buf in self.rules.reserved:
                t = "reserved"
            elif func:
                t = "function"
            elif buf in self.rules.values:
                t = "value"
            elif ((buf[0].isalpha() or (buf[0] == "_")) and self.bracket_follow()):
                t = "call"
            return True, buf, t
        return False, "", ""

    def get_next(self):
        for f in self.parsers:
            # Returns success, text result, type for formatting
            res, t, e = getattr(self, f)()
            if res:
                return t, e, e in self.rules.highlight

        return "", "", False
