# -*- coding = utf-8 -*-

from copy import deepcopy


def execute_mad(list, n=2):
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

    for j in range(0, len(list)):  # 调整极值到上下限
        if list[j] > median + n*mad:
            list[j] = median + n*mad
        elif list[j] < median - n*mad:
            list[j] = median - n*mad
    return list


if __name__ == '__main__':
    r = execute_mad([1,2,3,4,5,6,7], 2)
    print(r)