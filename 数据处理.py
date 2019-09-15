 #!/usr/bin/python
# -*- coding: UTF-8 -*-
# import xlrd
# import jieba 
# import xlsxwriter
# import re
# import numpy as np
# import random

# 数据规整化处理（城市维度、腐败程度维度、级别维度变量生产）
# def city():
# 	data1 = xlrd.open_workbook(r"筛选过腐败数据.xlsx")
# 	data2 = xlrd.open_workbook(r"cityandprovince.xlsx")
# 	data3 = xlrd.open_workbook(r"级别.xlsx")
# 	table1 = data1.sheet_by_index(0)
# 	table2 = data2.sheet_by_index(0)
# 	table3 = data3.sheet_by_index(1)
# 	workbook = xlsxwriter.Workbook("省城.xlsx")
# 	sheet = workbook.add_worksheet('1')		
# 	provinces = [province.strip() for province in table2.col_values(0)]
# 	cities = [cell.split() for cell in table2.col_values(1)]
# 	rank1 = [rank.strip() for rank in table3.col_values(0)[0].split("、")]
# 	rank2 = [rank.strip() for rank in table3.col_values(0)[1].split("、")]
# 	yans = [yan.strip() for yan in table3.col_values(1)]
# 	yansp = table3.col_values(2)
# 	chufs = table3.col_values(3)[:10]	
# 	chups = table3.col_values(4)[:10]
# 	nrow = table1.nrows
# 	print(chufs)
# 	print(chups)
# 	for n in range(nrow):
# 		row = table1.row_values(n)
# 		pro = row[0].strip()
# 		title = row[1]
# 		cities1 = cities[provinces.index(pro)]
# 		city = cities1[0]
# 		for city1 in cities1:
# 			if city1.replace("市","").replace("区","") in title:
# 				city = city1
# 				break
# 		rankt = 2
# 		rankm = ""
# 		for rank1a in rank1:
# 			if rank1a in title:
# 				rankt = 10
# 				rankm = rank1a
# 				print(title + " : " +rankm)
# 				break
# 		if rankt == 2:
# 			for rank2a in rank2:
# 				if rank2a in title:
# 					rankt = 6
# 					rankm = rank2a
# 					break

# 		text = row[3]
# 		yanp = 1
# 		yanpp = ""
# 		for yan in yans:
# 			if yan in text:
# 				yanpp += ";" + yan
# 				yanp += yansp[yans.index(yan)]
# 		p = 1
# 		f = ""
# 		for chuf in chufs:
# 			if chuf in text:
# 				p += chups[chufs.index(chuf)]
# 				f += ";" + chuf
# 		sheet.write(n,0,pro)
# 		sheet.write(n,1,city)
# 		sheet.write(n,9,title)
# 		sheet.write(n,2,rankt)
# 		sheet.write(n,3,rankm)
# 		sheet.write(n,4,row[7])
# 		sheet.write(n,5,yanp)
# 		sheet.write(n,6,yanpp)
# 		sheet.write(n,7,p)
# 		sheet.write(n,8,f)
# 	workbook.close()
# city()


# # 腐败程度及级别按省份和时间合并
# def zong():
# 	data1 = xlrd.open_workbook(r"省城.xlsx")	
# 	table1 = data1.sheet_by_index(0)
# 	workbook = xlsxwriter.Workbook("终.xlsx")
# 	sheet = workbook.add_worksheet('1')
# 	nrow = table1.nrows
# 	citys = []
# 	zhi = []
# 	fu = []
# 	for n in range(nrow):
# 		row = table1.row_values(n)
# 		cd = row[0]+";"+row[4]
# 		if cd not in citys:
# 			citys.append(cd)
# 			zhi.append(row[2])
# 			fu.append(float(row[5]))
# 		else:
# 			index = citys.index(cd)
# 			fu[index] = (fu[index]*zhi[index]+row[2]*float(row[5]))/(zhi[index]+row[2])
# 			zhi[index] += row[2]
# 	for n in range(len(zhi)):
# 		city1 = citys[n].split(";")		
# 		sheet.write(n,0,city1[0])
# 		sheet.write(n,1,city1[1])
# 		sheet.write(n,2,zhi[n])
# 		sheet.write(n,3,fu[n])
# 	workbook.close()
# zong()
from statsmodels.tsa.arima_model import ARMA
import statsmodels as sm
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
 
if __name__ == '__main__':
    mpl.rcParams['font.sans-serif'] = 'SimHei'
    mpl.rcParams['axes.unicode_minus'] = False
    data=pd.read_csv('yuce.csv',header=0,names=['date','peo_num'],nrows=70)
    print(data["date"].values[0])
    data = pd.Series(data["peo_num"].values, index=pd.DatetimeIndex(data["date"].values, freq='D'))
    decomposition=seasonal_decompose(data,model='additive')
    trend=decomposition.trend
    seasonal=decomposition.seasonal
    residual=decomposition.resid
    #对三部分分别进行拟合
    trend.dropna(inplace=True)
    trend_diff=trend.diff(periods=2)
    trend_diff.dropna(inplace=True)
    #分别对三部分进行拟合z
    #order_trend=sm.tsa.stattools.arma_order_select_ic(trend_diff)['bic_min_order']
    order_trend=(3,2)
    model_trend=ARMA(trend_diff,order_trend)
    result_trend=model_trend.fit()
    predict_trend=result_trend.predict()+trend.shift(2)
    forecast_trend,_,_=result_trend.forecast(11)
    forecast_trend=pd.Series(forecast_trend,index=pd.DatetimeIndex(start='2018/5/1',end='2019/5/1',freq='MS'))
    trend_predict=pd.concat([predict_trend,forecast_trend],axis=0)
    for i in range(11,0,-1):
        trend_predict.values[-i]+=trend_predict[-i-2]
    value_seasonal=[]
    for i in range(5):
        value_seasonal.append(seasonal.values[i])
    forecast_seasonal=pd.Series(value_seasonal,index=pd.DatetimeIndex(start='2019/1/1',end='2019/5/1',freq='MS'))
    seasonal_predict=pd.concat([seasonal,forecast_seasonal],axis=0)
 
    residual.dropna(inplace=True)
    order_residual=sm.tsa.stattools.arma_order_select_ic(residual)['bic_min_order']
    model_residual=ARMA(residual,order_residual)
    result_residual=model_residual.fit()
    predict_residual=result_residual.predict()
    forecast_residual,_,_=result_residual.forecast(11)
    forecast_residual=pd.Series(forecast_residual,\
                                index=pd.DatetimeIndex(start='2018/5/1',end='2019/5/1',freq='MS'))
    residual_predict=pd.concat([predict_residual,forecast_residual],axis=0)
    test_data=trend_predict+seasonal_predict+residual_predict
    print(test_data)
    data.plot(label='train_data',legend=True)
    test_data.plot(label='forecast_data',legend=True)
    plt.show()