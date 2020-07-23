# -*- coding: utf-8 -*-

"""
@Created: 2020/7/20 11:40
@AUTH: MeLeQ
@Used: pass
"""

import time
from database.db_config import CalculationPeriod
from database.mysql_tool import MysqlDb


m1 = MysqlDb()
m2 = MysqlDb()


def get_product_id():
    """
    获取所有 sku 型号
    :return:
    """
    sql = 'select DISTINCT product_model from `sku_more_infos`;'
    m1.cursor.execute(sql)
    while True:
        res = m1.cursor.fetchone()
        yield res
        if not res:
            break
    return


def get_single_sku_info(product_model, start_date):
    """
    获取当前查询周期下该sku的全部数据信息
    :return:
    """
    date_before = time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))-3600*24*CalculationPeriod))
    if not product_model:
        return []
    product_model = product_model[0]
    sql = f"select * from sku_more_infos where product_model='{product_model}' and update_time BETWEEN '{date_before}' and '{start_date}';"
    m2.cursor.execute(sql)
    res = m2.cursor.fetchall()
    return res


def get_sku_infos(start_date):
    for sku_id in get_product_id():
        res = get_single_sku_info(sku_id, start_date)
        yield sku_id[0], res
    m1.close()
    m2.close()


if __name__ == '__main__':
    for i in get_sku_infos("2020-02-01"):
        print(i)