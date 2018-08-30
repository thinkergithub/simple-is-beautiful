#-*- coding: UTF-8 -*-
import requests
import re
import uuid
#from bs4 import BeautifulSoup
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
headers = {'User-Agent': agent}
session = requests.session()

def login(account, pwd):

	login_url = 'http://10.3.8.211/'
	post_data = {
	'DDDDD': account,
	'upass': pwd,
	'0MKKey': ''
	}

	login_page = session.post(login_url, post_data, headers=headers)
	pattern_span = r'<span.*>(.*)</span>'
	status = re.findall(pattern_span, login_page.text)[0].encode('utf-8')
	return status


def write_html(content):
	with open('buptNet.html', 'w') as f:
		f.write(content)


def dataCount():
	data_url = 'http://10.3.8.211/'

	data_content = session.get(data_url, headers=headers).text

	pattern_flow = r"flow='(\d*)\s*'"
	flow_str = re.findall(pattern_flow, data_content)[0]
	flow = float(flow_str)
	flow0 = flow % 1024
	flow1 = int(flow - flow0)
	flow3 = "."
	decimal_temp = str(round(flow0/1024, 3))
	decimal_pattern = r'0.(\d*)'
	decimal_num = re.findall(decimal_pattern, decimal_temp)[0]
	Used_internet_traffic = str(flow1 / 1024 )+ flow3 + decimal_num
	return Used_internet_traffic


def get_mac_add():
	mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
	return ":".join([mac[e:e+2] for e in range(0,11,2)])
	

def output():
	my_mac_add = ""
	account = ''
	pwd = ''
	mac_add = get_mac_add()
	if my_mac_add == mac_add:
		status = login(account, pwd)
		if status == "登&nbsp;录&nbsp;成&nbsp;功":
			data_used = dataCount()
			total_data = 20 * 1024
			data_unused = float(total_data) - float(data_used)
			print "Used traffic: " + data_used + " MByte"
			print "Remaining traffic: " + str(data_unused) + " MByte"
			if data_unused > 1000:
				print "美滋滋！有流量看小猪佩奇啦".decode('utf-8')
				raw_input()
			else:
				print "额，没流量刷网页啦".decode('utf-8')
				raw_input()
		else:
			print "请检查网络连接情况".decode('utf-8')
	else:
		print "请检查MAC地址".decode('utf-8')	


if __name__ == '__main__':
	output()
		
