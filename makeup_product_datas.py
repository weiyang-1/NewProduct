# -*- coding: utf-8 -*-

"""
@Created: 2020/7/22 16:54
@AUTH: MeLeQ
@Used: pass
"""


from database.db_config import OriginalTestTable, OriginalSearchTestTable, FullTestTable
from database.mysql_tool import MysqlDb
from units.simple_tools import gene_date_by_day
import numpy as np


m1 = MysqlDb()


def get_product_id(table_name):
    """
    获取所有 sku 型号
    :return:
    """
    sql = f'select DISTINCT product_model from `{table_name}`;'
    m1.cursor.execute(sql)
    while True:
        res = m1.cursor.fetchone()
        yield res
        if not res:
            break
    return


def make_products_data():
    """
    INSERT INTO `sku_more_infos` VALUES("sku1100111sa1", "mic", "ic", 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1,2,3, "2020-06-01")
    :return:
    """
    m = MysqlDb()

    # 遍历所有sku  查询该sku的所有数据
    # 一次判断上下两条数据的日期  日期只差>1 则需要按照前一条数据补充  补充的条数为缺失的条数
    # 补充规则为上一条的记录数据  修改日期
    for product_id in get_product_id(OriginalTestTable):
        if isinstance(product_id, tuple):
            search_sql = f"select * from `{OriginalTestTable}` where product_model='{product_id[0]}' order by update_time;"
            m.cursor.execute(search_sql)
            res_list = m.cursor.fetchall()
            for i in range(len(res_list)-1):
                print(res_list[i])
                product_model, brand_name, catalog, price, stock, update_time_before = res_list[i]
                product_model_after, brand_name_after, catalog_after, price_after, stock_after, update_time_after = res_list[i+1]
                # 判断日期之差
                date_list = gene_date_by_day(str(update_time_before), str(update_time_after))
                print(date_list)
                if len(date_list) >= 2:
                    for date_next in date_list[1:]:
                        insert_sql = f""" INSERT INTO `{OriginalTestTable}` VALUES("{product_model}", "{brand_name}", "{catalog}", {price}, {stock}, "{date_next}");"""
                        print(insert_sql)
                        m.cursor.execute(insert_sql)
                        m.conn.commit()
    m.close()
    return


def make_search_data():
    """
    INSERT INTO `sku_more_infos` VALUES("sku1100111sa1", "mic", "ic", 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1,2,3, "2020-06-01")
    :return:
    """
    m = MysqlDb()

    # 遍历所有sku  查询该sku的所有数据
    # 一次判断上下两条数据的日期  日期只差>1 则需要按照前一条数据补充  补充的条数为缺失的条数
    # 补充规则为 全部为0 增加日期
    for product_id in get_product_id(OriginalSearchTestTable):
        if isinstance(product_id, tuple):
            search_sql = f"select * from `{OriginalSearchTestTable}` where product_model='{product_id[0]}' order by update_time;"
            m.cursor.execute(search_sql)
            res_list = m.cursor.fetchall()
            for i in range(len(res_list)-1):
                print(res_list[i])
                product_model, lc_search, lc_bom, jlc_bom, eda_person, eda_search, easy_bom, update_time_before = res_list[i]
                product_model_after, lc_search_after, lc_bom_after, jlc_bom_after, eda_person_after, eda_search_after, easy_bom_after, update_time_after = res_list[i+1]
                # 判断日期之差
                date_list = gene_date_by_day(str(update_time_before), str(update_time_after))
                print(date_list)
                if len(date_list) >= 2:
                    for date_next in date_list[1:]:
                        insert_sql = f""" INSERT INTO `{OriginalSearchTestTable}` VALUES("{product_model}", 0, 0, 0, 0, 0, 0, "{date_next}");"""
                        print(insert_sql)
                        m.cursor.execute(insert_sql)
                        m.conn.commit()
    m.close()
    return


def make_more_product_data():
    """
    根据商品信息表  生成完整的商品信息  对应的表为 FullTestTable = "sku_more_infos"
    :return:
    """
    m = MysqlDb()
    for product_id in get_product_id(OriginalTestTable):
        if isinstance(product_id, tuple):
            search_sql = f"select * from `{OriginalTestTable}` where product_model='{product_id[0]}' order by update_time;"
            m.cursor.execute(search_sql)
            res_list = m.cursor.fetchall()
            # 第一天记录  也就是所有数据计算的起始点
            product_model_first, brand_name_first, catalog_first, price_first, stock_first, update_time_first = res_list[0]
            # 所有的数据都从第二天开始计算数值

            # 计算波动值
            stock_list = []  # 库存波动
            price_list = []  # 价格波动
            stock_price_list = []  # 库存金额波动
            sales_counts_list = []  # 销量波动
            sales_money_list = []  # 销售额波动

            for i in range(0, len(res_list)-1):
                # 昨日 数据
                product_model_before, brand_name_before, catalog_before, price_before, stock_before, update_time_before = res_list[i]
                # 今日 数据
                product_model_today, brand_name_today, catalog_today, price_today, stock_today, update_time_today = res_list[i+1]
                # 判断日期之差  今日与第一日
                date_list = gene_date_by_day(str(update_time_first), str(update_time_today))
                coast_day = len(date_list)
                # 计算参数值
                day_sales_money = 0  # 销售额
                day_sales_count = 0  # 销量
                day_sales_stock_rate = 0  # 销存比
                day_stock_price = 0  # 库存金额
                stock_change = 0  # 库存波动
                price_change = 0  # 价格波动
                sale_money_change = 0  # 销售额波动
                stock_money_change = 0  # 库存金额波动
                sales_counts_change = 0  # 销量波动
                average_stock_develop = 0  # 库存平均增长
                average_stock_money_develop = 0  # 库存金额平均增长
                average_price_develop = 0  # 价格平均增长
                average_sales_counts_develop = 0  # 销量平均增长
                average_sales_money_develop = 0  # 销售额平均增长

                day_sales_count = stock_before - stock_today if (stock_today - stock_before) < 0 else 0
                day_sales_money = day_sales_count * price_today
                day_sales_stock_rate = day_sales_money/stock_before if stock_before>0 else 0
                day_stock_price = price_today * stock_today

                stock_list.append(stock_today)
                price_list.append(price_today)
                stock_price_list.append(day_stock_price)
                sales_counts_list.append(day_sales_count)
                sales_money_list.append(day_sales_money)

                stock_change = np.std(stock_list)
                price_change = np.std(price_list)
                sale_money_change = np.std(sales_money_list)
                stock_money_change = np.std(stock_price_list)
                sales_counts_change = np.std(sales_counts_list)

                average_stock_develop = (stock_list[-1] - stock_list[0]) / coast_day
                average_stock_money_develop = (stock_price_list[-1] - stock_price_list[0]) / coast_day
                average_price_develop = (price_list[-1] - price_list[0]) / coast_day
                average_sales_counts_develop = (sales_counts_list[-1] - sales_counts_list[0]) / coast_day
                average_sales_money_develop = (sales_money_list[-1] - sales_money_list[0]) / coast_day

                # 插入数据
                insert_sql = f""" INSERT INTO `{FullTestTable}` VALUES("{product_model_today}", "{brand_name_today}", "{catalog_today}", {day_sales_money}, {day_sales_count}, {price_today}, {stock_today}, {day_sales_stock_rate}, {day_stock_price}, {stock_change}, {price_change}, {sale_money_change}, {stock_money_change}, {sales_counts_change}, {average_stock_develop}, {average_stock_money_develop},{average_price_develop},{average_sales_counts_develop}, {average_sales_money_develop},"{update_time_today}");"""
                print(insert_sql)
                m.cursor.execute(insert_sql)
                m.conn.commit()
    m.close()
    return


if __name__ == '__main__':
    # 补充sku信息的缺省值  价格 库存
    # make_products_data()
    # 补充搜索记录数据的缺省值  各渠道搜索数
    # make_search_data()
    make_more_product_data()