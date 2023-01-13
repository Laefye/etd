TOKEN_TABLE = 'TABLE'
TOKEN_FIELD = 'FIELD'
TOKEN_METHOD = 'METHOD'
TOKEN_ARG = 'ARG'
TOKEN_SQL = 'SQL'

TOKEN_SQL_PART = 'SQL_PART'
TOKEN_SQL_TABLE = 'TABLE'
TOKEN_SQL_TABLE_FIELD = 'FIELD'
TOKEN_SQL_TABLE_VARIABLE = 'VARIABLE'

class SQL:
    def __init__(self, text) -> None:
        self.text = text
        self.tokens = []
        self.i = -1
    
    def _c(self):
        return self.text[self.i]

    def _cf(self):
        self.i += 1
        if self.i < len(self.text):
            return True
        return False

    def parseSqlPart(self):
        part = ''
        while self._cf():
            if self._c() in {'$', '&'}:
                self.i -= 1
                break
            part += self._c()
        self.tokens.append({
            't': TOKEN_SQL_PART,
            'part': part,
        })


    def parseField(self):
        field = ''
        while self._cf():
            if self._c() in {' ', ',', ')'}:
                self.i -= 1
                break
            field += self._c()
        self.tokens.append({
            't': TOKEN_SQL_TABLE_FIELD,
            'field': field,
        })

    def parseVariable(self):
        variable = ''
        while self._cf():
            if self._c() in {' ', ',', ')'}:
                self.i -= 1
                break
            variable += self._c()
        self.tokens.append({
            't': TOKEN_SQL_TABLE_VARIABLE,
            'field': variable,
        })

    def parse(self):
        while self._cf():
            if self._c() == '$':
                self.parseVariable()
            elif self._c() == '&':
                self.parseField()
            else:
                self.i -= 1
                self.parseSqlPart()

        return self.tokens

class Tokenizer:
    def __init__(self, text) -> None:
        self.text = text
        self.tokens = []

    def parse(self) -> None:
        lines = self.text.split('\n')
        for line in lines:
            if line == '':
                continue
            self.parseTableToken(line)
            self.parseMethodToken(line)
            self.parseArgToken(line)
            self.parseFieldToken(line)
            self.parseSQLToken(line)
        return self.tokens

    def parseTableToken(self, line) -> None:
        tabs = line.count('\t')
        line = line.replace('\t', '')
        if not line.startswith(TOKEN_TABLE):
            return
        words = line.split(' ')
        self.tokens.append({
            't': TOKEN_TABLE,
            'name': words[1],
            's': tabs
        })

    def parseFieldToken(self, line) -> None:
        tabs = line.count('\t')
        line = line.replace('\t', '')
        if not line.startswith(TOKEN_FIELD):
            return
        words = line.split(' ')
        self.tokens.append({
            't': TOKEN_FIELD,
            'name': words[2],
            'type': words[1],
            's': tabs
        })

    def parseMethodToken(self, line) -> None:
        tabs = line.count('\t')
        line = line.replace('\t', '')
        if not line.startswith(TOKEN_METHOD):
            return
        words = line.split(' ')
        self.tokens.append({
            't': TOKEN_METHOD,
            'name': words[2],
            'type': words[1],
            's': tabs
        })
    
    def parseSQLToken(self, line) -> None:
        tabs = line.count('\t')
        line = line.replace('\t', '')
        if not line.startswith(TOKEN_SQL):
            return
        words = line.split(' ')
        self.tokens.append({
            't': TOKEN_SQL,
            'query': SQL(' '.join(words[1:])).parse(),
            's': tabs
        })

    def parseArgToken(self, line) -> None:
        tabs = line.count('\t')
        line = line.replace('\t', '')
        if not line.startswith(TOKEN_ARG):
            return
        words = line.split(' ')
        self.tokens.append({
            't': TOKEN_ARG,
            'type': words[1],
            'name': words[2],
            's': tabs
        })