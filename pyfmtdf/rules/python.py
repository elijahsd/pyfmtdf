
class rules(object):
    spaces = [" ", "\t"]
    reserved = ["pass", "break", "continue", \
        "global", "nonlocal", \
        "assert", "del", "import", \
        "from", "as", "if", "elif", "else", "while", "for", "in", \
        "with", "try", "except", "finally", "return", "raise", \
        "def", "class", "lambda", \
        "or", "and", "not", \
        "yield", \
    ]
    f = ["def", "class"]
    values = ["True", "False", "None"]
    types = []
    ops = "=+-*@/%&|^<>:!~\\"
    brackets="[]{}()"
    numbers = "0123456789"
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_"
    comment = [["#", "\n", ""]]
    comment_string = [["\"\"\"", "\"\"\"", ""], ["'''", "'''", ""]]
    string = [["\"", "\"", "\\"], ["'", "'", "\\"]]
    fields = ".,;"
    highlight = ["function"]
