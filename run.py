# -*- coding: utf-8 -*-

"""
@Created: 2020/7/20 11:27
@AUTH: MeLeQ
@Used: pass
"""

import time
from database.db_config import EffectiveDigits
from units.simple_tools import gene_date_by_day
from core.get_sku_info import get_sku_infos
from core.convert_to_dataframe import get_source_datas


def start_project(start_date, end_date):
    """
    start project
    :param start_date: run start date ---> 2020-06-01
    :param end_date: run end date --- > 2020-06-30
    :return:

     # 1. 逐条获取sku信息
    # 2. 确定计算周期T内的该sku的所有因子的值
    # 3. 计算该sku所有因子的值
        # 3.0 每个因子数据进行异常值处理
        # 3.1 计算每个因子的方差 判断是否需要保留
        # 3.2 计算存留的因子的相关性  两两相关则保留
        # 3.3 对多个相关因子做姜维处理，尽可能把多个维度降低到更少的维度
    # 4. 计算最终sku当前得分
    # 5. 保存结果到结果表 todo
    """
    current_counts = 0
    day_list = gene_date_by_day(start_date, end_date)
    print(day_list)
    for c_date in day_list:
        print(f"c_date is: {c_date}")
        next_date = time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.strptime(c_date, "%Y-%m-%d")))+3600*24))
        print(f"next date is:{next_date}")
        for sku_id, infos in get_sku_infos(c_date):
            current_counts += 1
            print(f"current_counts is: {current_counts}")
            # 计算结果保留6位有效数字
            marks = round(get_source_datas(infos), EffectiveDigits)
            print(f"{sku_id}  {marks}  {next_date}")
            time.sleep(0.001)


if __name__ == '__main__':
    start_project("2020-02-01", "2020-02-28")