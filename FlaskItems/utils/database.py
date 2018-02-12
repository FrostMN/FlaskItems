import datetime
import time

import FlaskItems.utils.secrets as secrets
import config
from FlaskItems.models.schema import schema
# from FlaskItems.models.items import User

import MySQLdb

sql_host = config.MYSQL_HOST
sql_port = int(config.MYSQL_PORT)
sql_pwd = config.MYSQL_PASSWORD
sql_usr = config.MYSQL_USER
sql_db = config.MYSQL_DB

db = MySQLdb.connect(host=sql_host, port=sql_port, user=sql_usr, passwd=sql_pwd, db=sql_db)


def execute_query(qry, params=None):
    if params:
        with db.cursor() as cur:
            try:
                cur.execute(qry, params)
                db.commit()
            except MySQLdb.MySQLError as e:
                db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e
    else:
        with db.cursor() as cur:
            try:
                cur.execute(qry)
                db.commit()
            except Exception as e:
                db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e


def execute_queries(qry, params=None):
    if params:
        with db.cursor() as cur:
            try:
                cur.executemany(qry, params)
                db.commit()
            except MySQLdb.MySQLError as e:
                db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e
    else:
        with db.cursor() as cur:
            try:
                cur.executemany(qry)
                db.commit()
            except Exception as e:
                db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e


def get_rs(qry, params=None):
    if params:
        with db.cursor() as cur:
            try:
                cur.execute(qry, params)
                rs = cur.fetchall()
                if len(rs) == 1:
                    rs = rs[0]
                db.commit()
                return rs
            except MySQLdb.MySQLError as e:
                db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e
    else:
        with db.cursor() as cur:
            try:
                cur.execute(qry)
                rs = cur.fetchall()
                db.commit()
                return rs
            except Exception as e:
                db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e


def _init_db():
    for qry in schema:
        execute_query(qry)


if __name__ == '__main__':
    _init_db()
