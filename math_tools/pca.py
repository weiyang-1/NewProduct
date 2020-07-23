# -*- coding = utf-8 -*-
'''
对传入的两个数组(list类型)进行降维处理，返回降维后的矩阵。
本例中要求：1、每个list代表一个维度(因子)，列代表样本
@:param  array:需要进行降维处理的矩阵
@:param  k:需要降到的维度
@:return   :降维后的结果数据
'''

import numpy as np


def do_pca(k, *list):
    try:
        arr = np.mat([*list]).T  #组合成为转置矩阵,行代表样本，列代表因子/维度
        reduce_avg_matrix = arr - arr.mean(axis=0)   #将原始数据按列去均值化
        cov_matrix = np.cov(reduce_avg_matrix.T)  #计算去均值化后的矩阵的协方差矩阵
        eigenvalue, eigenvector = np.linalg.eig(cov_matrix)  #计算标准化后的协方差矩阵的特征值与特征向量
        eigenvalueInd = np.argsort(eigenvalue)
        eigenvalueInd = eigenvalueInd[:-(k+1):-1]  #保留最大的前k个特征值
        finaleigvector = eigenvector[:,eigenvalueInd]  #对应的特征向量
        res = (reduce_avg_matrix * finaleigvector).T
        r = res.tolist()[0]
        return r
    except Exception as e:
        print(e)
        return []


if __name__ == '__main__':
    sr = do_pca(1, [2,3,4,5,6,7], [3,4,4,6,7,8])
    print(sr)