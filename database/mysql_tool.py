# -*- coding: utf-8 -*-

"""
@Created: 2020/7/17 15:17
@AUTH: MeLeQ
@Used: pass
"""

from pymysql import Connect
from database.db_config import MYSQL_DB


class MysqlDb(object):

    def __init__(self):
        self.conn = Connect(host=MYSQL_DB["host"], port=3306, user=MYSQL_DB["user"], password=MYSQL_DB["password"], database=MYSQL_DB["database"])
        self.cursor = self.conn.cursor()

    def search_one(self, sql):
        """
        search one then return
        :return:
        """
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            return res
        except Exception as e:
            print(e)

    def search_all(self, sql):
        """
        search all results
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            print(e)

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    # MysqlDb()
    pass
