import sys

class formatter(object):
    def __init__(self, palette):
        self.palette = palette

    def start(self):
        return "<pre>"

    def end(self):
        return "</pre>"

    def esc(self, text):
        text = text.replace("&" , "&amp;")
        text = text.replace("<" , "&lt;")
        text = text.replace(">" , "&gt;")
        return text

    def format(self, text, entity, bold):
        if entity not in self.palette.keys():
            print("ERROR: Unknown entity")
            sys.exit(2)
        if self.palette[entity] == "":
            return text
        return "<span class=\"\" style=\"color: {};\">{}{}{}</span>".format(self.palette[entity], bold and "<b>" or "", self.esc(text), bold and "</b>" or "")
