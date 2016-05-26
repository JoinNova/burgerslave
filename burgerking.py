# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cookielib
import urllib
import urllib2

BASE_URL = "https://kor.tellburgerking.com/"

jar = cookielib.FileCookieJar("cookies")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

request_num = 0

def init():
	code = ""
	while(True):
		code = raw_input('설문조사 코드 16자리를 입력해주세요 : ')
		if(len(code)==16):
			break
		print "코드를 다시 확인해주세요."
	print "초기화중입니다. 잠시만 기다려주세요."
	raw = opener.open(BASE_URL)
	read = raw.read()
	parsed = BeautifulSoup(read)
	data = {"JavaScriptEnabled":"1","FIP":"True","AcceptCookies":"Y"}
	data = urllib.urlencode(data)
	req = urllib2.Request(BASE_URL+str(parsed.find("form")['action']), data)
	raw = opener.open(req)
	read = raw.read()
	parsed = BeautifulSoup(read)
	data = {"JavaScriptEnabled":"1","FIP":"True","CN1":code[0:3],"CN2":code[3:6],"CN3":code[6:9],"CN4":code[9:12],"CN5":code[12:15],"CN6":code[15]}
	data = urllib.urlencode(data)
	req = urllib2.Request(BASE_URL+str(parsed.find("form")['action']), data)
	nextStep(req)

def nextStep(req):
	global request_num
	request_num += 1
	print "Request #"+str(request_num)
	raw = opener.open(req)
	read = raw.read()
	parsed = BeautifulSoup(read)
	if not parsed.find("div", { "class" : "Error" }):
		vc = parsed.find("p", { "class" : "ValCode" })
		if vc:
			print vc.getText()
		else:
			data = {}
			fns = parsed.find(attrs={"name": "PostedFNS"})['value']
			fns_list = fns.split('|')
			for posted in fns_list:
				data[posted] = 2
			ionf = parsed.find(attrs={"name": "IoNF"})['value']
			data["IoNF"] = ionf
			data["PostedFNS"] = fns
			data = urllib.urlencode(data)
			req = urllib2.Request(BASE_URL+str(parsed.find("form")['action']), data)
			nextStep(req)
	else:
		print "잘못된 코드입니다. 다시 시도해주세요. :("
		init()
init()
