# -*- coding: utf-8 -*-

"""
@Created: 2020/7/22 16:54
@AUTH: MeLeQ
@Used: pass
"""


from database.mysql_tool import MysqlDb
from units.simple_tools import gene_date_by_day

m1 = MysqlDb()


def get_product_id():
    """
    获取所有 sku 型号
    :return:
    """
    sql = 'select DISTINCT product_model from `sku_info`;'
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
    # 使用update语句进行补充，避免产生多条重复数据
    for product_id in get_product_id():
        if isinstance(product_id, tuple):
            search_sql = f"select * from sku_info where product_model='{product_id[0]}' order by update_time;"
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
                        insert_sql = f""" INSERT INTO `sku_info_copy` VALUES("{product_model}", "{brand_name}", "{catalog}", {price}, {stock}, "{date_next}");"""
                        print(insert_sql)
                        m.cursor.execute(insert_sql)
                        m.conn.commit()


if __name__ == '__main__':
    make_products_data()