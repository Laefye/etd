from compiler import *

def loads(file):
    c = ''
    with open(file, 'r') as f:
        c = f.read()
    c = Compiler(Tokenizer(c).parse())
    c.compile()
    return c.env