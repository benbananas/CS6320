import pandas as pd
import numpy as np

operands = [">", "<", "=", ">=", "<=", "!="]
operands_one_hots = np.diag(np.ones(6))
# nr_cols = 6  # total nr of [int] cols in both tables
cols_names = [
    "math score",
    "reading score",
    "writing score",
    "math score2",
    "reading score2",
    "writing score2",
]

""" Makes n queries randomly + uniformly

tables: 2 dataframes
table_names: list of two possible vals - 2 tables
n: number of queries to be generated
max_nr_preds: max number of predicates per query
"""


def generate_queries(
    tables, table_names, n=20000, max_nr_preds=1, cols_names=cols_names
):
    nr_cols = len(cols_names)

    def generate_query():
        sql_query = ""
        sql_query_vec = []

        # if join the first bit of sql query is 1 --> that is indicator of join
        # [join_bit]
        sql_query_vec.append(np.random.randint(0, 2))
        table_ind = np.random.randint(0, 2)

        # [join_bit, tb1_bit, tb2_bit]
        if sql_query_vec[0]:
            # You are joining --> select * from tb1, tb2 where tb1 == tb2
            sql_query = f"SELECT * FROM {table_names[0]}, {table_names[1]} WHERE country_code = code AND"
            sql_query_vec.extend([1, 1])  # <- if join, dont need AND_bit or OR_bit
        else:
            sql_query = f"SELECT * FROM {table_names[table_ind]} WHERE"
            if table_ind:
                sql_query_vec.extend([0, 1])
            else:
                sql_query_vec.extend([1, 0])

        # nr_predicates = {1,2}
        nr_predicates = (
            1 if sql_query_vec[0] else np.random.randint(1, max_nr_preds + 1)
        )

        # Need to edit this to be the columns of the tables in equation

        column = (
            np.random.choice(range(0, tables[table_ind].shape[1] - 1), nr_predicates)
            if table_ind == 0
            else np.random.choice(
                range(tables[table_ind].shape[1] - 1, nr_cols), nr_predicates
            )
        )
        # column = np.random.choice(['math score', 'reading score', 'writing score'], nr_predicates)

        # sign is either array of len 1 or 2
        # 6 operands
        sign = np.random.choice(range(6), nr_predicates)

        # Each loop should end in something like
        # [..., <columns_bits~nr_cols> <sign_bits~6> <value real>]
        for predicate in range(nr_predicates):
            value = np.random.randint(
                np.min(tables[table_ind][cols_names[column[predicate]]]),
                np.max(tables[table_ind][cols_names[column[predicate]]]),
            )
            if predicate == 0:
                sql_query += f" {table_names[table_ind] + '.' + cols_names[column[predicate]]} {operands[sign[predicate]]} {value}"
            else:
                if np.random.randint(0, 2):
                    sql_query += f" AND {table_names[table_ind] + '.' + cols_names[column[predicate]]} {operands[sign[predicate]]} {value}"
                    sql_query_vec.extend([1, 0])
                elif sql_query_vec[0]:  # if u r joining, we treat it as no extra AND
                    sql_query += f" AND {table_names[table_ind] + '.' + cols_names[column[predicate]]} {operands[sign[predicate]]} {value}"
                    sql_query_vec.extend([0, 0])
                else:
                    sql_query += f" OR {table_names[table_ind] + '.' + cols_names[column[predicate]]} {operands[sign[predicate]]} {value}"
                    sql_query_vec.extend([0, 1])

            tmp = [0] * nr_cols
            tmp[column[predicate]] = 1
            sql_query_vec.extend(tmp)

            tmp = [0] * len(operands)
            tmp[sign[predicate]] = 1
            sql_query_vec.extend(tmp)

            sql_query_vec.append(value)

        if nr_predicates == 1:
            sql_query_vec.extend([0] * (nr_cols + 6 + 1 + 2))

        return sql_query, sql_query_vec

    sqlQuery = []
    vectorQuery = []
    for i in range(n):
        sql_query, sql_query_vec = generate_query()
        sqlQuery.append(sql_query)
        vectorQuery.append(sql_query_vec)

    return sqlQuery, vectorQuery
