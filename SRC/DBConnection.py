#!/usr/bin/python

import MySQLdb as mdb
from sshtunnel import SSHTunnelForwarder

MOODLE_USERNAME = ''
MOODLE_PASSWORD = ''

serverName = 'mysqlsrv1.cs.tau.ac.il'
user = 'DbMysql03'
password = 'DbMysql03'
dbName = 'DbMysql03'


def execute_query(query, *kargs):
    """
    executes DB query
    :param query:
    :param kargs:
    :return:
    """
    rows = []
    with SSHTunnelForwarder(('nova.cs.tau.ac.il', 22), ssh_password=MOODLE_PASSWORD, ssh_username=MOODLE_PASSWORD,
                            remote_bind_address=('mysqlsrv1.cs.tau.ac.il', 3306)) as server:
        con = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='DbMysql03', passwd='DbMysql03')
        con.select_db('DbMysql03')
        cur = con.cursor()
        with con:
            cur = con.cursor()
            try:
                cur.execute(
                    query % kargs)  # query should be something like "SELECT %S FROM %S ..." and kargs are the params
                con.commit()

            except Exception as e:
                print(e)
                print("Error: failed executing/committing query")
                con.rollback()
                return

            try:
                rows = cur.fetchall()
            except Exception as e:
                print(e)
                print("Error: failed fetching data")

            cur.close()
    return rows
