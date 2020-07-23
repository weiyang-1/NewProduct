# -*- coding: utf-8 -*-

"""
@Created: 2020/7/22 16:54
@AUTH: MeLeQ
@Used: pass
"""


from database.db_config import OriginalTestTable, OriginalSearchTestTable
from database.mysql_tool import MysqlDb
from units.simple_tools import gene_date_by_day

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


if __name__ == '__main__':
    # 补充sku信息的缺省值  价格 库存
    make_products_data()
    # 补充搜索记录数据的缺省值  各渠道搜索数
    make_search_data()