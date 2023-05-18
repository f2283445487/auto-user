import os
import pymysql as pymysql
from dbutils.pooled_db import PooledDB


host = '8.222.33.249'
user = 'common_rw'
pw = 'P9tx$I7RNYJrAFv'
port = 9897

pool_db = PooledDB(
    creator=pymysql,
    maxconnections=5,
    mincached=1,
    maxcached=5,
    blocking=True,
    maxusage=None,
    ping=0,
    host=host,
    user=user,
    password=pw,
    # database="singa_origin",
    port=port,
    autocommit=True

)
db = pool_db.connection()
cur = db.cursor(pymysql.cursors.DictCursor)


def select(sql):
    cur.execute(sql)
    data = cur.fetchall()
    return data


def update(sql):
    try:
        cur.execute(sql)
    except Exception as e:
        return e
