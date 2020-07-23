# -*- coding: utf-8 -*-

"""
@Created: 2020/7/20 14:50
@AUTH: MeLeQ
@Used: pass
"""


import time
import numpy as np
from math_tools.mad import execute_mad
from math_tools.get_ic import get_rank_ic, get_rank_more
from math_tools.pca import do_pca
from math_tools.mad_std import execute_mad_std


def get_unification_data(data: list):
    """
    数据归一化处理
    :return:
    """
    min_data = min(data)
    denominator = max(data) - min_data
    new_data = [(i-min_data)/denominator for i in data]
    return new_data


def get_source_datas(datas):
    """
    1. 获取原始数据  转为np数组
    2. 获取销售额数据， 以此为参照因素
    3. 对原始数据进行， mad异常值处理，归一化处理，方差过滤，IC值过滤
    :return:
    """
    res_list = []
    for i in datas:
        if len(i) >= 10:
            line_list = list(i[3:-1])
            res_list.append(line_list)
    arr_data = np.array(res_list)
    # 1. 对原始数据去掉异常值
    # 遍历数组的每一列 计算方差  行数为 n 列数为 m
    n, m = arr_data.shape
    # 取第一列为销售额  保存为对比变量
    sales_money_list = list(arr_data[:,0])
    new_data = []  # 最终输出的列表
    variance_list = []  # 保存逐行计算的方差
    for i in range(0, m):
        # 过滤之后的数组为列表形式
        filter_list = execute_mad(list(arr_data[:,i]))
        # 将过滤后的结果归一化
        filter_list = get_unification_data(filter_list)
        new_data.append(filter_list)
        # 计算每一行数据的方差
        variance_line = np.std(filter_list)
        variance_list.append(variance_line)
    # 2. 过滤方差异常值
    save_index = execute_mad_std(variance_list)
    # print(f"std_checked len is:{len(save_index)}")
    std_checked_data = []
    for index_number in save_index:
        std_checked_data.append(new_data[index_number])
    # 3. 判断ic值 是否大于 0.05
    ic_checked_data = []
    for single_line in std_checked_data:
        # 单因素校验ic值取1  固定
        if get_rank_ic(1, single_line, sales_money_list) > 0.05:
            ic_checked_data.append(single_line)
    # print(f"ic checked len is:{len(ic_checked_data)}")
    corr_list = merge_factors(ic_checked_data, sales_money_list)
    return corr_list


def merge_factors(datas: list, control_group: list):
    """
    分别计算多个因素之间的相关性，并对有相关的因素做降维计算
    :param data:
    :return: 降维之后的数据
    """
    corr_list = []  # 强相关因素队列
    not_list = []  # 非强相关因素队列
    pca_list = []  # 降维之后的队列
    for i in range(0, len(datas)-1):
        # 多因子之间计算相关性需要设置t=1
        if get_rank_more(1, datas[i], datas[i+1])> 0.5:
            if datas[i] not in corr_list:
                corr_list.append(datas[i])
            if datas[i+1] not in corr_list:
                corr_list.append(datas[i+1])
            # 此因素做降维处理 将二维相关的
            pca_res = do_pca(1, datas[i], datas[i+1])
            pca_list.append(pca_res)
        else:
            if (datas[i] not in not_list) and (datas[i] not in corr_list):
                not_list.append(datas[i])
            if datas[i+1] not in not_list and (datas[+1] not in corr_list):
                not_list.append(datas[i+1])
    final_data = not_list + pca_list
    # print(f"corr len is:{len(corr_list)}")
    total_marks = merge_all_datas(final_data, control_group)
    return total_marks


def merge_all_datas(datas: list, control_group: list):
    """
    计算最终结果
    :return:
    """
    total_marks = 0
    for data in datas:
        ic_mark = get_rank_ic(1, data, control_group)
        total_marks += ic_mark*data[-1]
    return total_marks


if __name__ == '__main__':
    pass