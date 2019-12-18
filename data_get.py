import time,requests,re
import pandas as pd
from lxml import etree

# csv save path
csv_path = './data/'

# open html
url = 'http://www.tianqihoubao.com/aqi/'
headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36", }
response = requests.get(url, headers=headers)
html = response.text
response = etree.HTML(html)

# get city url
city_url_list = response.xpath('//div[@class="citychk"]//a/@href')
for city_url in city_url_list:
	
	# define csv files name;
	name = city_url.split('/')[2]
	name = name.split('.')[0]
	print('start get ' + name + ' PM2.5 data')
	
	# define csv name
	name = name + '.csv'
	
	# city_url
	city_url = 'http://www.tianqihoubao.com' + city_url
	# http://www.tianqihoubao.com/aqi/wuhan.html
	
	# open city html
	response = requests.get(city_url, headers=headers)
	html = response.text
	response = etree.HTML(html)
	
	# get months_url_list
	months_url_list = response.xpath('//div[@class="box p"]//a/@href')
	for months_url in months_url_list:
		
		# months_url
		months_url='http://www.tianqihoubao.com' + months_url
		
		# get PM2.5 data
		data = pd.read_html(months_url, header=0, encoding='gbk')[0]
		print(data)
		time.sleep(1)
		
		# write data to csv files
		data.to_csv(csv_path +name, mode='a', header=False)
	print(name + ' PM2.5 data write successfully!')
