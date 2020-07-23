# -*- coding: utf-8 -*-

"""
@Created: 2020/7/17 16:54
@AUTH: MeLeQ
@Used: pass
"""


import random
from database.mysql_tool import MysqlDb
from units.simple_tools import gene_date_by_day


def insert_products_data():
    """
    INSERT INTO `sku_more_infos` VALUES("sku1100111sa1", "mic", "ic", 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1,2,3, "2020-06-01")
    :return:
    """
    m = MysqlDb()

    # 随机生成10000个sku 商品编号以 随机字母 abd + 数字 + 随机字母  ---> acdv0001pchy
    # 类别 为前缀三位  品牌为后缀3位
    # 每个sku 生成指定日期的条数
    # 中间的结果全为随机数
    date_list = gene_date_by_day("2020-01-01", "2020-03-31")
    pro_key = "abcdefghigklmnopqrstuvwxyz"
    for count in range(10000):
        product_model = ""
        brand_name = ""
        catalog = ""
        for _ in range(6):
            brand_name += pro_key[random.randint(1, len(pro_key)-1)]
        for _ in range(6):
            catalog += pro_key[random.randint(1, len(pro_key))-1]
        product_model = brand_name + str(count*100) + catalog
        for date_time in date_list:
            # 给数值做随机
            day_sales_money = random.randint(1, 100000)*0.1
            day_sales_count = random.randint(1, 10000)
            day_price = random.randint(1, 10000)*0.001
            day_stock = random.randint(1, 100000)
            day_sales_stock_rate = random.randint(1, 1000)*0.01
            day_stock_price = random.randint(1, 1000000)*0.1
            stock_change = random.randint(1, 100000)*0.1
            price_change = random.randint(1, 10000)*0.1
            sale_money_change = random.randint(1, 100000)*0.1
            stock_money_change = random.randint(1, 100000)*0.1
            sales_counts_change = random.randint(1, 100000)*0.1
            average_stock_develop = random.randint(1, 100000)*0.1
            average_stock_money_develop = random.randint(1, 100000)*0.1
            average_price_develop = random.randint(1, 100000)*0.1
            average_sales_counts_develop = random.randint(1, 100000)*0.1
            # 执行插入数据库操作
            sql = f""" INSERT INTO `sku_more_infos` VALUES("{product_model}", "{brand_name}", "{catalog}", {day_sales_money}, {day_sales_count}, {day_price}, {day_stock}, {day_sales_stock_rate}, {day_stock_price}, {stock_change}, {price_change}, {sale_money_change}, {stock_money_change}, {sales_counts_change}, {average_stock_develop}, {average_stock_money_develop},{average_price_develop},{average_sales_counts_develop}, "{date_time}");"""
            print(f"sql is:{sql}")
            m.cursor.execute(sql)
            m.conn.commit()
    m.close()


if __name__ == '__main__':
    insert_products_data()