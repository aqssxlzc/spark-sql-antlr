
from unittest import TestCase
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Trees import Trees
from SparksqlLexer import SparksqlLexer
from SparksqlParser import SparksqlParser
from SparksqlVisitor import SparksqlVisitor


class CustomVisitor1(SparksqlVisitor):

    def __init__(self):
        super(CustomVisitor1, self).__init__()

    def visitSelect_statement(self, ctx:SparksqlParser.Select_statementContext):
        print('select begin')
        return self.visitChildren(ctx)


class CustomErrorListener(ErrorListener):

    def __init__(self):
        super(CustomErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception('Error: %s; Line: %s, Col: %s' % (msg, line, column))


class Parser1(object):

    def __init__(self):

        self.is_valid = False
        self.error = None
        self.tree = None
        self.tree_str = None

    def parse(self, sql):

        in_stream = InputStream(sql)
        lexer = SparksqlLexer(in_stream)
        token_stream = CommonTokenStream(lexer)

        try:

            parser = SparksqlParser(token_stream)
            parser._listeners = [CustomErrorListener()]
            self.tree = parser.root()
            self.tree_str = Trees.toStringTree(self.tree, None, parser)
            self.is_valid = True

        except Exception as ex:
            self.is_valid = False
            self.error = ex


sql_cases = [
    { 'sql': 'select * from table_0', 'expected': True },
    { 'sql': 'select a,b,c from table_0', 'expected': True },
    { 'sql': 'select m.a,m.b,m.c from table_0 as m', 'expected': True },
    { 'sql': 'select a, b from', 'expected': False },
    { 'sql': 'select a.c0, a.c1, b.c0, b.c1 from table_a as a, table_b as b where a.c0=b.c0', 'expected': True },
    { 'sql': 'select table_a.c0, table_a.c1, table_b.c0, table_b.c1 from table_a, table_b where table_a.c0=table_b.c0', 'expected': True }
]

class TestSqlCases(TestCase):

    def test_all_cases(self):

        for sql_case in sql_cases:

            sql = sql_case['sql']
            expected = sql_case['expected']

            p = Parser1()
            p.parse(sql)

            print("Given %s, Expected: %s, Sql: %s" % (p.is_valid, expected, sql))

    def test_case1(self):

        sql_case = sql_cases[0]
        sql = sql_case['sql']
        expected = sql_case['expected']

        p = Parser1()
        p.parse(sql)
        print(p.tree_str)

        self.assertEqual(p.is_valid, expected)

        visitor = CustomVisitor1()
        visitor.visit(p.tree)

        self.assertTrue(True)


