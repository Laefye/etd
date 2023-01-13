from tokenizer import *

class Sql:
    def __init__(self) -> None:
        self.method = None
        self.query = []

class Arg:
    def __init__(self) -> None:
        self.method = None
        self.name = ''
        self.type = ''

class Method:
    def __init__(self) -> None:
        self.table = None
        self.env = None
        self.sql = []
        self.args = []
        self.type = ''
        self.name = ''
        self.type = ''

    def getField(self, field):
        if '.' in field:
            path = field.split('.')
            table = None
            if path[0] == '&':
                table = self.table
            else:
                table = self.env.tableByName(path[0])
            field = table.fieldByName(path[1])
            return '`%s`.`%s`' % (table.name, field.name)
        else:
            if field == '&':
                return '`%s`' % self.table.name
            else:
                return '`%s`' % self.env.tableByName(field).name
        
    def getArgByName(self, name):
        for i in self.args:
            if i.name == name:
                return i

    def execute(self, var, tableVar):
        query = ''
        for i in self.sql:
            for q in i.query:
                if q['t'] == TOKEN_SQL_PART:
                    query += q['part']
                if q['t'] == TOKEN_SQL_TABLE_FIELD:
                    query += self.getField(q['field'])
                if q['t'] == TOKEN_SQL_TABLE_VARIABLE:
                    if not q['field'].startswith('&'):
                        arg = self.getArgByName(q['field'])
                        query += var(arg.name, arg.type)
                    else:
                        field = self.table.fieldByName(q['field'][2:])
                        query += tableVar(field.name, field.type)

        return query
        
        

class Field:
    def __init__(self) -> None:
        self.table = None
        self.name = ''
        self.type = ''

class Table:
    def __init__(self) -> None:
        self.env = None
        self.name = ''
        self.fields = []
        self.methods = []
    
    def fieldByName(self, name):
        for i in self.fields:
            if i.name == name:
                return i

class Env:
    def __init__(self) -> None:
        self.tables = []
        self.methods = []

    def tableByName(self, name):
        for i in self.tables:
            if i.name == name:
                return i
    
class Compiler:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.i = -1
        self.env = Env()
    
    def _c(self):
        return self.tokens[self.i]

    def _cf(self):
        self.i += 1
        if self.i < len(self.tokens):
            return True
        return False
    
    def compile(self):
        while self._cf():
            if self._c()['t'] == TOKEN_TABLE:
                self.compileTable(self.env)
            elif self._c()['t'] == TOKEN_METHOD:
                self.compileMethod(None, self.env)

    def compileTable(self, env):
        table = Table()
        table.env = env
        table.name = self._c()['name']
        s = self._c()['s']
        while self._cf():
            if self._c()['s'] <= s:
                self.i -= 1
                break
            if self._c()['t'] == TOKEN_FIELD:
                self.compileField(table)
            if self._c()['t'] == TOKEN_METHOD:
                self.compileMethod(table, env)
        env.tables.append(table)
            

    def compileField(self, table):
        field = Field()
        field.table = table
        field.type = self._c()['type']
        field.name = self._c()['name']
        table.fields.append(field)

    def compileMethod(self, table, env):
        method = Method()
        method.table = table
        method.env = env
        method.name = self._c()['name']
        method.type = self._c()['type']
        s = self._c()['s']
        while self._cf():
            if self._c()['s'] <= s:
                self.i -= 1
                break
            if self._c()['t'] == TOKEN_ARG:
                self.compileArg(method)
            if self._c()['t'] == TOKEN_SQL:
                self.compileSql(method)
        if table == None:
            env.methods.append(method)
        else:
            table.methods.append(method)
    
    def compileArg(self, method):
        arg = Arg()
        arg.method = method
        arg.type = self._c()['type']
        arg.name = self._c()['name']
        method.args.append(arg)

    def compileSql(self, method):
        sql = Sql()
        sql.method = method
        sql.query = self._c()['query']
        method.sql.append(sql)