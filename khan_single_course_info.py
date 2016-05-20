from bs4 import BeautifulSoup
import requests
import pymysql
from datetime import date,datetime

def get_course_detail(url):
    url = 'http://open.163.com/special/Khan/finance.html'
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    series = soup.select('table.m-clist > tr > td.u-ctitle > a')
