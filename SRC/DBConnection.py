#!/usr/bin/python
import decimal

import MySQLdb as mdb
from sshtunnel import SSHTunnelForwarder
import json

MOODLE_USERNAME = ''
MOODLE_PASSWORD = ''

serverName = 'mysqlsrv1.cs.tau.ac.il'
user = 'DbMysql03'
password = 'DbMysql03'
dbName = 'DbMysql03'


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


def execute_query(query, *kargs):
    """
    executes DB query
    :param query:
    :param kargs:
    :return:
    """
    rows = []
    # With SSH
    with SSHTunnelForwarder(('nova.cs.tau.ac.il', 22), ssh_password=MOODLE_PASSWORD, ssh_username=MOODLE_USERNAME,
                            remote_bind_address=('mysqlsrv1.cs.tau.ac.il', 3306)) as server:
        con = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='DbMysql03', passwd='DbMysql03')
        ##### end With SSH

        # Without SSH
        # con = mdb.connect(host='mysqlsrv1.cs.tau.ac.il', port=3306, user='DbMysql03', passwd='DbMysql03')
        ##### end Without SSH

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
            json_data = []
            if 'INSERT' not in query:
                try:
                    row_headers = [x[0] for x in cur.description]
                    rows = cur.fetchall()
                except Exception as e:
                    print(e)
                    print("Error: failed fetching data")

                for result in rows:
                    json_data.append(dict(zip(row_headers, result)))

            cur.close()

    return json.dumps(json_data, cls=DecimalEncoder)

    # return rows
