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
"""
| product_model     | brand_name | catalog | day_price | day_stock | update_time |
| kajdwj001wkddkw	|     kajdk  | wkddk   | 1.35	   | 40	       | 2020-01-03  |
| kajdwj001wkddkw	|     kajdk  | wkddk   | 1.35	   | 40	       | 2020-01-04  |
| kajdwj001wkddkw	|     kajdk  | wkddk   | 1.35	   | 40	       | 2020-01-05  |
"""

# 搜索数据测试原始数据表
OriginalSearchTestTable = "search_info"
"""
| product_model     | lc_search | lc_bom | jlc_bom | eda_person | eda_search | easy_bom | update_time |
| kajdkwj001wkddkw	|     10	| 20	 | 30	   | 40	        |     50     | 60	    | 2020-01-03  |
| kajdkwj001wkddkw	|     10	| 20	 | 30	   | 40	        |     50     | 60	    | 2020-01-04  |
| kajdkwj001wkddkw	|     10	| 20	 | 30	   | 40	        |     50     | 60	    | 2020-01-05  |
"""

# sku信息测试完整数据表
FullTestTable = "sku_more_infos"
"""
| product_model     | brand_name | catalog | day_sales_money | day_sales_count | day_price | day_stock | day_sales_stock_rate | day_stock_price | stock_change | price_change| sales_money_change | stock_money_change | sales_counts_change | average_stock_develop | average_stock_money_develop | average_price_develop | average_sales_counts_develop | uodate_time| 
| kajdwj001wkddkw	|     kajdk  | wkddk   |      926.2	     | 7325            | 7.764     | 6124      | 9.84                 | 73759.8         | 7168.1       | 195.7       | 174.4              | 8085.6             | 483.3               | 3432.4                | 3169.7                      | 8182.9                | 206.7                        | 2020-01-03 | 
| kajdwj001wkddkw	|     kajdk  | wkddk   |      924.2	     | 7324            | 7.764     | 6124      | 9.84                 | 73759.8         | 7168.1       | 195.7       | 174.4              | 8085.6             | 483.3               | 3432.4                | 3169.7                      | 8182.9                | 206.7                        | 2020-01-04 |  
| kajdwj001wkddkw	|     kajdk  | wkddk   |      925.2	     | 7329            | 7.764     | 6124      | 9.84                 | 73759.8         | 7168.1       | 195.7       | 174.4              | 8085.6             | 483.3               | 3432.4                | 3169.7                      | 8182.9                | 206.7                        | 2020-01-05 | 
"""


# 搜索数据测试完整数据表
FullSearchTestTable = "search_infos"
"""
| product_model     | search_counts | update_time |
| kajdkwj001wkddkw	|     100	    | 2020-01-03  |
| kajdkwj001wkddkw	|     110	    | 2020-01-04  |
| kajdkwj001wkddkw	|     120	    | 2020-01-05  |
"""

# sku测试结果数据表
FinalResultTestTable = "final_result"
"""
| product_model     | final_marks   | update_time |
| kajdkwj001wkddkw	|     0.121245  | 2020-01-03  |
| kajdkwj001wkddkw	|     0.542235  | 2020-01-04  |
| kajdkwj001wkddkw	|     0.784512  | 2020-01-05  |
"""