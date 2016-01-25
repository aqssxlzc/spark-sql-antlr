
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
            self.tree = parser.select_statement()
            self.tree_str = Trees.toStringTree(self.tree, None, parser)
            self.is_valid = True

        except Exception as ex:
            self.is_valid = False
            self.error = ex


sql_cases = [
    { 'sql': 'select * from table_0', 'expected': True }
    ,{ 'sql': 'select a,b,c from table_0', 'expected': True }
    ,{ 'sql': 'select m.a,m.b,m.c from table_0 as m', 'expected': True }
    ,{ 'sql': 'select a, b from', 'expected': False }
    ,{ 'sql': 'select a.c0, a.c1, b.c0, b.c1 from table_a as a, table_b as b where a.c0=b.c0', 'expected': True }
    ,{ 'sql': 'select table_a.c0, table_a.c1, table_b.c0, table_b.c1 from table_a, table_b where table_a.c0=table_b.c0', 'expected': True }

    ,{ 'sql': 'select a.c0, a.c1, b.c0, b.c1 from table_a as a inner join table_b as b on a.c0=b.c0', 'expected': True }
    ,{ 'sql': 'select a.c0, a.c1, b.c0, b.c1 from table_a as a left join table_b as b on a.c0=b.c0', 'expected': True }
    ,{ 'sql': 'select a.c0, a.c1, b.c0, b.c1 from table_a as a right join table_b as b on a.c0=b.c0', 'expected': True }
    ,{ 'sql': 'select a from dummy as t0 union select b from fake t1', 'expected': True }
    ,{ 'sql': 'select t1.* from (SELECT c0 FROM n0.t0 WHERE (c1 >= 50 AND c1 < 65)) as t1 where t1.c0 > 9778 and t1.c0< 9800', 'expected': True }
    ,{ 'sql': "with t3 as (SELECT distinct t1.c0 FROM n0.t0 as t1 INNER JOIN n0.t00 as t2 on t2.c1= t1.c0) select count(*) from t3", 'expected': True }
    ,{ 'sql': 'select vcf.*, cv.highest_clinical_significance, cv.hgvs, cv.rs_id, snpf.annotation_impact, snpf.feature_type, snpf.feature_id from vcf.samples as vcf left join annotation.clinvar_rollup cv on (vcf.chromosome = cv.chromosome and vcf.position = cv.position and vcf.ref = cv.ref and vcf.alt = cv.alt) left join annotation.cadd_flatten cadd on (vcf.chromosome = cadd.chromosome and vcf.position = cadd.position and vcf.ref = cadd.ref and vcf.alt = cadd.alt) left join annotation.snpeff_flatten snpf on (vcf.chromosome = snpf.chromosome and vcf.position = snpf.position and vcf.ref = snpf.ref and vcf.alt = snpf.alt) where sample_id = 176444255', 'expected': True}
    ,{ 'sql': "SELECT chromosome ,position ,ref ,alt ,sum(allele_count) / (count (distinct sample_id)) as allele_frequency FROM (SELECT chromosome ,position ,ref ,alt ,sample_id ,CASE WHEN gt0 = '1' AND gt1 = '1' then 2 else 1 END as allele_count FROM vcf.samples s WHERE s.filter = 'PASS') v GROUP BY chromosome ,position ,ref ,alt limit 10", 'expected': True }
    #,{ 'sql': '', 'expected': True }
]

class TestSqlCases(TestCase):

    def test_all_cases(self):

        for sql_case in sql_cases:

            sql = sql_case['sql']
            expected = sql_case['expected']

            p = Parser1()
            p.parse(sql)

            print("Result %s, Expected: %s, Sql: %s" % (p.is_valid, expected, sql))

        print('end')

    def test_case1(self):

        sql_case = sql_cases[12]
        sql = sql_case['sql']
        expected = sql_case['expected']

        p = Parser1()
        p.parse(sql)
        self.assertEqual(p.is_valid, expected)

        print(p.tree_str)
        visitor = CustomVisitor1()
        visitor.visit(p.tree)

        self.assertTrue(True)

    def test_af(self):

        sql = """
        SELECT
            chromosome
            ,position
            ,ref
            ,alt
            ,sample_id
            ,CASE WHEN gt0 = '1' AND gt1 = '1' then 2 else 1 END as allele_count
        FROM
            vcf.samples as s
        WHERE
            s.filter = 'PASS'
        """

        sql = """
        SELECT
            v.chromosome
            ,v.position
            ,v.ref
            ,alt
            ,sum(allele_count) / (count (distinct sample_id)) as allele_frequency
        FROM Tab1
        GROUP BY
            chromosome
            ,position
            ,ref
            ,alt
        """

        sql = """
        SELECT
            v.chromosome
            ,v.position
            ,v.ref
            ,alt
            ,sum(allele_count) / (count (distinct sample_id)) as allele_frequency
        FROM (
            SELECT
                chromosome
                ,position
                ,ref
                ,alt
                ,sample_id
                ,CASE WHEN gt0 = '1' AND gt1 = '1' then 2 else 1 END as allele_count
            FROM
                vcf.samples as s
            WHERE
                s.filter = 'PASS') as v
        GROUP BY
            chromosome
            ,position
            ,ref
            ,alt
        limit 10
        """

        # sql = """
        # select a.c0, a.c1, b.c0, b.c1 from table_a as a inner join table_b as b on a.c0=b.c0
        # """

        p = Parser1()
        p.parse(sql)
        if p.is_valid:
            print(p.tree_str)

        self.assertTrue(True)
