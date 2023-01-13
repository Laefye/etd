import etd
import sys

env = etd.loads(sys.argv[1])

def tp(a):
    if a.startswith('~'):
        return '[]*' + a[1:]
    if 'varchar' in a:
        return 'string'
    return a

def getQuery(method):
    params = ['']
    def var(name, type):
        params[0] += ', ' + name
        return '?'
    def varTable(name, type):
        params[0] += ', t.' + name
        return '?'
    return (method.execute(var, varTable), params[0])

def arguments(method):
    arguments = []
    for arg in method.args:
        arguments.append(arg.name + ' ' + tp(arg.type))
    return ','.join(arguments)

print('package db')
print('')

for table in env.tables:
    print('type %s struct {' % table.name)
    for field in table.fields:
        print('\t%s %s `db="%s"`' % (field.name, tp(field.type), field.name))
    print('}')
    print('')
    for method in table.methods:
        if method.type == 'NONE':
            print('func (t *%s) %s(%s) {' % (table.name, method.name, arguments(method)))
            print('\tdb.Exec("%s"%s)' % getQuery(method))
        else:
            print('func (t *%s) %s(%s) %s {' % (table.name, method.name, arguments(method), tp(method.type)))
            if not method.type.startswith('~'):
                print('\tvalue := &%s{}' % method.type)
                print('\tif db.Get(value, "%s"%s) != nil {' % getQuery(method))
                print('\t\treturn nil')
                print('\t}')
                print('\treturn value')
            else:
                print('\tvalues := []*%s{}' % method.type[1:])
                print('\tdb.Select(&value, "%s"%s)' % getQuery(method))
                print('\treturn values')
        print('}')
        print()


for method in env.methods:
    if method.type == 'NONE':
        print('func %s(%s) {' % (method.name, arguments(method)))
        print('\tdb.Exec("%s"%s)' % getQuery(method))
    else:
        print('func %s(%s) %s {' % (method.name, arguments(method), tp(method.type)))
        if not method.type.startswith('~'):
            print('\tvalue := &%s{}' % method.type)
            print('\tif db.Get(value, "%s"%s) != nil {' % getQuery(method))
            print('\t\treturn nil')
            print('\t}')
            print('\treturn value')
        else:
            print('\tvalues := []*%s{}' % method.type[1:])
            print('\tdb.Select(&value, "%s"%s)' % getQuery(method))
            print('\treturn values')
    print('}')
    print()
