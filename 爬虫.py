 #!/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd
import jieba 
import xlsxwriter
from urllib import request
from bs4 import BeautifulSoup
import random
import requests
import re
import time
from selenium import webdriver
import js2xml
from lxml import etree
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# jieba.load_userdict("D:/学习/大三上/数据挖掘/作业/小组/dict.txt")

# seg_list = jieba.cut("贵州省政府原党组成员、副省长蒲波严重违纪违法被开除党籍和公职", cut_all=False)

# print("/ ".join(seg_list))

# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

# workbook = xlsxwriter.Workbook("./爬取内容海南.xlsx")
# sheet = workbook.add_worksheet('1')
# urlbase = "http://www.gzdis.gov.cn/gzdt/jlsc"

# 数据存数据库
# Base = declarative_base()
# class Zhengce(Base):
# 	__tablename__ = "zhengce"
# 	id = Column(Integer, primary_key = True)
# 	title = Column(String(255))
# 	releaseTime = Column(String(255))
# 	content = Column(String(255))
# class Href(Base):
# 	__tablename__ = "href"
# 	id = Column(Integer, primary_key = True)
# 	href =  Column(String(255))
# engine = create_engine('mysql+pymysql://root:0509gudu@localhost:3306/homework?charset=utf8')	
# Base.metadata.create_all(engine)
# DBSession = sessionmaker(bind = engine)

# browser = webdriver.Chrome()

# browser.get("http://www.nmgjjjc.gov.cn/category/scdc/zzqjwjwqwfb.html?t=15450972827#1")
# input_first = browser.find_element_by_id("DeqhURb")
# print(input_first)

# def get_ip_list():
# 	web_data = requests.get('http://www.xicidaili.com/nn/', headers={
# 		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
# 	})
# 	soup = BeautifulSoup(web_data.text, 'lxml')
# 	ips = soup.find_all('tr')
# 	ip_list = []
# 	for i in range(1, len(ips)):
# 		ip_info = ips[i]
# 		tds = ip_info.find_all('td')
# 		ip_list.append(tds[1].text + ':' + tds[2].text)
# 	return ip_list
# def get_random_ip(ip_list):
# 	proxy_list = []
# 	for ip in ip_list:
# 		proxy_list.append('http://' + ip)
# 	proxy_ip = random.choice(proxy_list)
# 	proxies = {'http': proxy_ip}
# 	return proxies

# 代理和访问头
def fix(url):
	proxy_list = [
		"180.110.6.1:3128",
		"125.40.109.154:31610",
		"219.234.5.128:3128",
		"116.7.176.75:8118",
		"113.128.140.208:8118",
		"223.145.212.41:8118",
		"115.46.79.78:8123",
		"182.88.213.122:8123",
		"123.185.220.83:8118",
		"180.119.65.150:1133",
		"171.38.91.123:8123",
		"121.228.52.61:3128",
		"121.31.143.13:8123"
	]	
	proxy1 = {'http':random.choice(proxy_list)}
	#设置代理
	proxy=request.ProxyHandler(proxy1)
	#创建一个opener
	opener=request.build_opener(proxy)
	#添加User Angent
	my_headers = [
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
	   	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	   	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
	   	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
	   	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
	   	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
	   	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
	   	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
	   	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
	   	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
	   	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
	   	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
	   	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
	   	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
	   	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	   	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
	   ]
	opener.addheaders = [('User-Agent',random.choice(my_headers)),
						('Accept-Language', 'zh-CN,zh;q=0.8'),
						('Cookie','BDTUJIAID=d42f1396fb2dd605205bbb77c849470d; doctaobaocookie=1; 360docsn=TR2PL6ETN37LIVND; Hm_lvt_d86954201130d615136257dde062a503=1543849087,1543908405,1545438293,1545466894; Hm_lpvt_d86954201130d615136257dde062a503=1545466894'),
						('Connection','keep-alive'),
						('Host','www.360doc.com'),
						('Pragma','no-cache'),
						('Upgrade-Insecure-Requests','1')
						]
	#将opener安装为全局
	request.install_opener(opener)
	# 使用安装好的Opener
	try:
		global response 
		response = request.urlopen(url)			
	except:
		# 如果不成功，休息10秒再来
		print("连接错误")
		time.sleep(30)
		fix(url)
	#用urlopen打开网页

	# soup1 = BeautifulSoup(request.urlopen(url).read(), 'lxml')
	# print(soup1.select("#content_views")[0].get_text())
	return response
# fix("https://blog.csdn.net/weixin_40188147/article/details/78167071")
# 内蒙古
# def spider(urlbase):
# 	url = urlbase + "/category/scdc/gmsjwjwqwfb.html?t=1545138258264" 
# 	soup1 = BeautifulSoup(request.urlopen(url).read(), 'lxml')

# 	script = soup1.select(".c-list-con > script")[0].string
# 	text = js2xml.parse(script, encoding='utf-8', debug=False)
# 	tree = etree.HTML(js2xml.pretty_print(text))
# 	sources = tree.xpath('//property[@name="source"]/string/text()')
# 	contentUrls = tree.xpath('//property[@name="href"]/string/text()')
# 	titles = tree.xpath('//property[@name="title"]/string/text()')
# 	releaseTimes = tree.xpath('//property[@name="showDate"]/string/text()')
# 	contentnum = range(len(contentUrls))
# 	for i in contentnum:
# 		time.sleep(3)
# 		soup2 = BeautifulSoup(request.urlopen(contentUrls[i]).read(), 'lxml')
# 		content = soup2.select(".c-content-con")[0].get_text()
# 		sheet.write(i, 0, titles[i])
# 		sheet.write(i, 1, releaseTimes[i])
# 		sheet.write(i, 2, content)
# 		sheet.write(i, 3, sources[i])
# spider(urlbase)
# workbook.close()

#海南
# def spider(urlbase):
# 	url = urlbase + "djcf_sggb.php?ncount=150&nbegin=0" 
# 	response = fix(url)
# 	soup1 = BeautifulSoup(response.read(), 'lxml')
# 	list1 = soup1.select("#mainrconlist > ul")[0].select("li")
# 	sheetrow = 0
# 	response.close()
# 	for li in list1:
# 		session = DBSession()
# 		title = li.select("h1")[0].get_text()
# 		releaseTime = li.select("p")[0].get_text()
# 		href = li.select("h1 > a")[0]["href"]
# 		time.sleep(20)	
# 		if urlbase not in href:
# 			href = urlbase + href
# 		response = fix(href)	
# 		soup2 = BeautifulSoup(response.read(), 'lxml')
# 		response.close()
# 		try:
# 			content = soup2.select("#artcon")[0].get_text()
# 			content = content[:content.index("我也发言")].strip()
# 			zhengce = Zhengce(title = title, content = content, releaseTime = releaseTime)
# 			session.add(zhengce)
# 			session.commit()
# 			session.close()
# 			print(href)
# 		except:
# 			print("herf错误")
# 			hrefc = Href(href = href)
# 			session.add(hrefc)
# 			session.commit()
# 			session.close()
# 			continue

# spider(urlbase)
# workbook.close()

# soup1 = BeautifulSoup(request.urlopen(urlbase+"/index.html").read(), 'lxml')
# li = soup1.select(".list01 > li")[0]
# script = li.select('script')[0].string
# title = script[script.index('str_3 = "')+9:script.index('";',script.index('str_3 = "'))]
# href = script[script.index('str_1 = "')+10:script.index('";',script.index('str_1 = "'))]
# soup2 = BeautifulSoup(request.urlopen(urlbase+'/201812/t20181211_2766154.html').read(), 'lxml')
# source = soup2.select(".btnr > p")[0].string
# source = source[source.index("信息来源")+5:]
# content = soup2.select("#textBox")[0].get_text()
# content = content[:content.index("分享到：")].strip()
# print("source : " +source)
# print("content : " +content)

# 贵州
# def spider(url):
# 	global urlbase
# 	global sheetrow
# 	soup1 = BeautifulSoup(request.urlopen(url).read(), 'lxml')
# 	lis = soup1.select(".list01 > li")
# 	for li in lis:
# 		script = li.select('script')[0].string
# 		title = script[script.index('str_3 = "')+9:script.index('";',script.index('str_3 = "'))]
# 		href = script[script.index('str_1 = "')+10:script.index('";',script.index('str_1 = "'))]
# 		releaseTime = li.select('span')[0].string
# 		time.sleep(20)
# 		try:
# 			soup2 = BeautifulSoup(request.urlopen(urlbase+href).read(), 'lxml')
# 		except:
# 			print("herf错误")
# 			lis.append(li)
# 			continue
# 		source = soup2.select(".btnr > p")[0].string
# 		source = source[source.index("信息来源")+5:]
# 		content = soup2.select("#textBox")[0].get_text()
# 		content = content[:content.index("分享到：")].strip()		
# 		sheet.write(sheetrow, 0, title)
# 		sheet.write(sheetrow, 1, releaseTime)
# 		sheet.write(sheetrow, 2, content)
# 		sheet.write(sheetrow, 3, source)
# 		sheetrow += 1

# spider(urlbase+"/index.html")
# for i in range(1,15):
# 	url = urlbase + "/index_"+str(i) +".html"
# 	spider(url)
# workbook.close()

# 中纪委
# def spider(url):
# 	soup1 = BeautifulSoup(request.urlopen(url).read(), 'lxml')
# 	lilist = soup1.select('li')
# 	for li in lilist:
# 		global sheetrow
# 		lia = li.select("a")[0]
# 		title = lia.string
# 		contentUrl = urlbase + lia['href'][1:]
# 		soup2 = BeautifulSoup(request.urlopen(contentUrl).read(), 'lxml')
# 		em = soup2.select('.daty_con > em')
# 		source = em[0].string[3:]
# 		releaseTime = em[1].string[5:]
# 		content = soup2.select(".TRS_Editor")[-1].get_text()
# 		sheet.write(sheetrow, 0, title)
# 		sheet.write(sheetrow, 1, releaseTime)
# 		sheet.write(sheetrow, 2, content)
# 		sheet.write(sheetrow, 3, source)
# 		sheetrow += 1

# spider(urlbase + "/index_8.html")
# # for a in range(1,2):
# # 	url = urlbase + "/index_" + str(a) + ".html"
# # 	spider(url)
# workbook.close()
	
# def paragraph():
# 	workbook = xlsxwriter.Workbook("分割段落.xlsx")
# 	sheet = workbook.add_worksheet('1')
# 	data = xlrd.open_workbook(r"爬取内容.xlsx")
# 	table = data.sheet_by_index(0)
# 	num = table.nrows
# 	for n in range(num):
# 		row = table.row_values(n)
# 		text = row[2]
# 		title = row[0]
# 		province = ["北京市","天津市","上海市","重庆市","河北省","山西省","辽宁省","吉林省","黑龙江省","江苏省","浙江省","安徽省","福建省","江西省","山东省","河南省","湖北省","湖南省","广东省","海南省","四川省","贵州省","云南省","陕西省","甘肃省","青海省","内蒙古自治区","广西壮族自治区","西藏自治区","宁夏回族自治区","新疆维吾尔自治区","香港特别行政区","澳门特别行政区"]
# 		for pro in province:
# 			if pro in title:
# 				title = title.replace(pro,'')
# 				sheet.write(n,0,pro)
# 		sheet.write(n,1,title)
# 		sheet.write(n,2,row[1])
# 		print(n)
# 		ri = re.compile('日前.*').search(text)
# 		if ri:
# 			sheet.write(n,3,ri.group())
# 		jing = re.compile('经查.*').search(text)
# 		if jing:
# 			sheet.write(n,4,jing.group())
# 		ren = re.compile('经查.*\\n.*').search(text)
# 		if ren:
# 			if len(ren.group().split()) > 1:
# 				sheet.write(n,5,ren.group().split()[1])
# 	workbook.close()
# paragraph()

def cityspyder():
	soup1 = BeautifulSoup(fix("http://www.360doc.com/content/18/0417/19/11561215_746441668.shtml").read(), 'lxml')
	artContent = soup1.select("#artContent > div:nth-child(7) > div > p")
	print(artContent)
cityspyder()

# def paragraph():
# 	workbook = xlsxwriter.Workbook("广西自治区分段.xlsx")
# 	sheet = workbook.add_worksheet('1')
# 	data = xlrd.open_workbook(r"广西自治区.xlsx")
# 	table = data.sheet_by_index(0)
# 	num = table.nrows
# 	for n in range(num):
# 		row = table.row_values(n)
# 		sheet.write(n,0,row[0])
# 		sheet.write(n,1,row[1])
# 		sheet.write(n,2,row[2])
# 		text = row[3]		
# 		ri = re.compile("日前.*', '").search(text)
# 		if ri:
# 			sheet.write(n,3,ri.group())
# 		jing = re.compile("经查.*").search(text)
# 		if jing:
# 			jings = jing.group().split("', '")
# 			sheet.write(n,4,jings[0])
# 			if len(jings) > 1:	
# 				sheet.write(n,5,jings[1])
# 	workbook.close()
# paragraph()

# def jiangsu():
# 	workbook = xlsxwriter.Workbook("广东省筛.xlsx")
# 	sheet = workbook.add_worksheet('1')
# 	data = xlrd.open_workbook(r"广东省.xlsx")
# 	table = data.sheet_by_index(0)
# 	num = table.nrows
# 	citys = ['江苏','常州','徐州','南京','淮安','南通','宿迁','无锡','扬州','盐城','苏州','泰州','镇江','连云港','海安','常熟','邳州','新沂','溧阳','张家港','宜兴','太仓','昆山','如皋','海门','启东','东台','高邮','仪征','丹阳','扬中','句容','靖江','兴化','泰兴','江阴','如东','宝应','建湖','阜宁','射阳','滨海','响水','涟水','盱眙','金湖','沭阳','泗阳','泗洪','东海','灌云','灌南','睢宁','沛县','丰县']
# 	sheetrow = 0
# 	for n in range(num):
# 		row = table.row_values(n)
# 		title = row[1]
# 		for city in citys:
# 			if city in title:
# 				sheet.write(sheetrow,0,row[0])
# 				sheet.write(sheetrow,1,title)
# 				sheet.write(sheetrow,2,row[2])
# 				sheet.write(sheetrow,3,row[3])
# 				sheet.write(sheetrow,4,row[4])
# 				sheet.write(sheetrow,5,row[5])
# 				sheetrow += 1
# 				break
# 	workbook.close()
# jiangsu()
# def yanzhongchengdu():
# 	data1 = xlrd.open_workbook(r"总.xlsx")
# 	data2 = xlrd.open_workbook(r"yanzhongchengdu.xlsx")
# 	table1 = data1.sheet_by_index(0)
# 	table2 = data2.sheet_by_index(0)
# 	num = 0
# 	workbook = xlsxwriter.Workbook("./guang.xlsx")
# 	sheet = workbook.add_worksheet('1')	
# 	num = table1.nrows
# 	ci = table2.col_values(0)
# 	ranks = table2.col_values(1)
# 	for n in range(num):
# 		row = table1.row_values(n)
# 		pin = row[3]
# 		ping = ""
# 		rank = 0
# 		for c in ci:
# 			if c in pin:
# 				ping +=";"+c
# 				rank +=ranks[ci.index(c)]
# 		sheet.write(n,0,rank)
# 		sheet.write(n,1,pin)
# 		sheet.write(n,2,ping)
# 	workbook.close()
# yanzhongchengdu()