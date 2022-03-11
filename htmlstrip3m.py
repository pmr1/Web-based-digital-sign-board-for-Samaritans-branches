'''
HTml parsing
cf https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
this strips out html tags
dependencies
python
   HTMLParser
   StringIO
'''

from html.parser import HTMLParser
from io import StringIO

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False  # false
        self.convert_charrefs= False # true
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    
    

