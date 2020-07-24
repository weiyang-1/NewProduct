# -*- coding: utf-8 -*-

"""
@Created: 2020/7/17 16:56
@AUTH: MeLeQ
@Used: pass
"""

import datetime


def gene_date_by_day(day_begin, day_end):
    """
    :param day_begin: 起始日期
    :param day_end: 结束日期
    :return: 中间所有日期  左开右闭 【 ）
    """
    begin = datetime.datetime.strptime(day_begin, '%Y-%m-%d')
    end = datetime.datetime.strptime(day_end, '%Y-%m-%d')
    date_list = [day_begin]
    while begin < end:
        begin += datetime.timedelta(days=1)
        date_list.append(begin.strftime('%Y-%m-%d'))
    return date_list[:-1]


if __name__ == '__main__':
    r = gene_date_by_day("2020-02-23", "2020-02-24")
    print(r)