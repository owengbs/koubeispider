# coding:utf-8
import cookielib
import mechanize
import urllib

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.open('http://k4w.cn/user/index.html')
br.select_form(nr=0)
br.form['mail'] = 'xxxx@xxx.com'
br.form['password'] = 'xxxxxxx'
br.submit()
