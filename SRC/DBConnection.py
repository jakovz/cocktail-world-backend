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
            cur.execute(query, kargs)  # query should be something like "SELECT %S FROM %S ..." and kargs are the params
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
