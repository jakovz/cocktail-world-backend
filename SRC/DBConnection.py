#!/usr/bin/python

import MySQLdb as mdb

serverName = 'test623'
user = 'testuser'
password = 'localhost'
dbName = 'testdb'

con = mdb.connect(serverName, user, password, dbName);
cur = con.cursor(mdb.cursors.DictCursor)


def execute_query(query, *kargs):
    """
    executes DB query
    :param query:
    :param kargs:
    :return:
    """
    with con:

        try:
            # query should be something like "SELECT %S FROM %S ..." and kargs are the params
            cur.execute(query, kargs)
            cur.commit()

        except:
            cur.rollback()

        rows = cur.fetchall()

        for row in rows:
            print (row["Id"], row["Name"])

        for i in range(cur.rowcount):
            row = cur.fetchone()
            print (row[0], row[1])

        cur.close()


def execute_query_2(query, **kwargs):
    # Accepts arguments in order of:
    # SELECT=[select_args], FROM=[from_args], WHERE=[where_args]
    arguments = []
    for key, value in kwargs.items():
        arguments.append(value)
    # arguments should contain a list of 3 lists:
    # [ [select_args], [from_args], [where_args] ]
    # Mabye more lists if we have "order by.." , and stuff like that
