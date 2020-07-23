# -*- coding = utf-8 -*-

from copy import deepcopy
from database.db_config import Mad_N


def execute_mad_std(list):
    """
    传入list是需要进行离群值处理的list参数
    @:param  list:需要进行离群值处理的数据
    @:param  n:控制上下限范围，默认为2
    @:return result
    """
    def get_median(list1):
        """
        返回中位数的方案
        :param list1: 需要获取中位数的数据
        :return:
        """
        list2 = deepcopy(list1)
        list2.sort()
        half = len(list2)//2
        return (list2[half] + list2[~half])/2

    median = get_median(list)  # 获取原始数据集的中位数
    temp = deepcopy(list)  # 用于计算并存储原始数据集到中位数的距离，即偏差值
    for i in range(0, len(temp)):
        temp[i] = abs(temp[i] - median)

    mad = get_median(temp)  # 绝对偏差值的中位数
    index_list = []
    for j in range(0, len(list)):  # 调整极值到上下限
        if list[j] >= median - Mad_N*mad:
            # 输出索引
            index_list.append(j)
    return index_list


if __name__ == '__main__':
    r = execute_mad_std([1, 1000,1002,1003,1004,1005,1006,1007])
    print(r)