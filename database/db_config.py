# -*- coding: utf-8 -*-

"""
@Created: 2020/7/17 15:19
@AUTH: MeLeQ
@Used: pass
"""

# mysql 数据库配置
MYSQL_DB = {
    "host": "192.168.154.132",
    "user": "yangwei",
    "password": "123456",
    "database": "new_product",
    "charset": "utf-8"
}

# 设置计算周期 默认为30 天 只能为整数
CalculationPeriod = 30

# 设置mad计算N的取值 用来设置异值数据上下限 默认为2
Mad_N = 2

# 最终计算结果保留有效数字的位数  只能为整数
EffectiveDigits = 6

# t计算周期 设置ic计算周期  含义为： 1天  一周 半月  一月  半年  一季度  120天
Tcycle = [1, 7, 15, 30, 60, 90, 120]

# sku信息测试原始数据表
OriginalTestTable = "sku_info"

# sku信息测试完整数据表
FullTestTable = "sku_more_infos"

# 搜索数据测试原始数据表
OriginalSearchTestTable = "search_info"

# 搜索数据测试完整数据表
FullSearchTestTable = "search_infos"

# sku测试结果数据表
FinalResultTestTable = "final_result"
