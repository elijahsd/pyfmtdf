
class rules(object):
    spaces = [" ", "\t"]
    reserved = ["abstract", "continue", "for", "new", "switch", \
                "assert", "default", "goto", "synchronized", \
                "do", "if", "private", \
                "break", "implements", "protected", "throw", \
                "else", "import", "public", "throws", \
                "case", "instanceof", "return", "transient", \
                "catch", "extends", "try", \
                "final", "interface", "static", \
                "finally", "strictfp", \
                "native", "super", \
                "while", \
    ]
    f = ["class", "package"]
    values = ["true", "false", "null", "boolean", "this", "double", "byte", \
                "enum", "int", "short", "char", "var", "long", "void", "const", \
                "float", "volatile", ]
    ops = "=+-*/%&|^<>?:!~\\"
    brackets="[]{}()"
    numbers = "0123456789"
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_@"
    comment = [["//", "\n", ""], ["/*", "*/" , ""]]
    comment_string = []
    string = [["\"", "\"", "\\"], ["'", "'", "\\"]]
    fields = ".,;"
    highlight = ["function"]
