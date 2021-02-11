from difflib import unified_diff
from html.parser import HTMLParser

class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.text += "\n"

class checker(object):
    def __init__(self):
        pass

    def check(f, buf):
        i = ""
        with open(f, 'r') as fd:
            i = fd.read()
        f = HTMLFilter()
        f.feed(buf)

        a = i.splitlines()
        b = f.text.splitlines()
        for ind, s in enumerate(a):
            tmp = list(s.replace("\t", "    "))
            for ti, c in enumerate(tmp):
                if c == " ":
                    tmp[ti] = "\xA0"
                else:
                    break
            a[ind] = ''.join(tmp)
        if a == b:
            return True
        diff = unified_diff(a, b, lineterm='')
        print('\n'.join(diff))
        return False
