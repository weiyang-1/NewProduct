# -*- coding: utf-8 -*-

"""
@Created: 2020/7/21 10:19
@AUTH: MeLeQ
@Used: pass
"""


import pandas as pd
import numpy as np
from copy import deepcopy
from database.db_config import Tcycle


def get_rank_ic(t, list1: list, list2: list):
    """
    计算并返回list的IC值
    @:param  list1:需要进行计算的list
    @:param  list2:进行对比的list
    @:param  t:时间周期，默认为1，可选7,15,30,90,120
    本例要求：1、list1、list2元素个数相同；2、t是大于1的正整数
    @:return   :IC值
    :param t: 计算周期需小于列表长度
    :param list1: 列表1
    :param list2: 列表2
    """

    # 列表1与列表2的长度需完全一致 否则输出的线性相关性为0
    if len(list1) != len(list2):
        return 0
    elif len(list1) <= t:
        return 0
    return pd.DataFrame({'A': list1[t-1::t][:-1], 'B': list2[t-1::t][1:]}).corr('spearman')['A']['B']


def get_IR(list1, list2, wt):
    if wt <= 1: return None
    cycle = deepcopy(Tcycle)
    for i in range(0, len(cycle)):
        if wt < cycle[i]:
            cycle = cycle[0:i]
            break
        continue
    aIC = []
    for a_t in cycle:
        aIC.append(get_rank_ic(a_t, list1, list2))

    return np.mean(aIC)/np.var(aIC)


def get_rank_more(t, list1: list, list2: list):
    """
    计算并返回list的IC值
    @:param  list1:需要进行计算的list
    @:param  list2:进行对比的list
    @:param  t:时间周期，默认为1，可选7,15,30,90,120
    本例要求：1、list1、list2元素个数相同；2、t是大于1的正整数
    @:return   :IC值
    :param t: 计算周期需小于列表长度
    :param list1: 列表1
    :param list2: 列表2
    """

    # 列表1与列表2的长度需完全一致 否则输出的线性相关性为0
    if len(list1) != len(list2):
        return 0
    elif len(list1) <= t:
        return 0
    return pd.DataFrame({'A': list1[t-1::t], 'B': list2[t-1::t]}).corr('spearman')['A']['B']