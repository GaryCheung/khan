from bs4 import BeautifulSoup
import requests
import pymysql
from datetime import date,datetime
import re

def delete_today_data(config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM khan WHERE date = '%s'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_entire_course():
    url = 'http://open.163.com/khan/'
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    courses = soup.select('div.m-cate.m-cate1 > div.g-container > div.g-row.g-limitrow.j-row > div.g-cell1.g-card1 > a > h5')
    urls = soup.select('div.m-cate.m-cate1 > div.g-container > div.g-row.g-limitrow.j-row > div.g-cell1.g-card1 > a')
    url = []
    course = []
    for course_trans,url_trans in zip(courses,urls):
        course.append(course_trans.get_text())
        url.append(url_trans.get('href'))
    return course,url

def mysql_insert(course,url,config):
    for i in range(1,len(course)):
        connection = pymysql.connect(**config)
        try:
            with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'INSERT INTO khan (date, course, url) VALUES (%s, %s, %s)'
                cursor.execute(sql, (present_date, course[i], url[i]))
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            connection.commit()
        finally:
            connection.close()

present_date = datetime.now().date()

config_php = {
    'host':'127.0.0.1',
    'port':8889,
    'user':'root',
    'password':'root',
    'db':'study',
    'charset':'utf8',
    'unix_socket':'/Applications/MAMP/tmp/mysql/mysql.sock'
}

config_python = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'19860112',
    'db':'study',
    'charset':'utf8'
}

delete_today_data(config_python)
result = get_entire_course()
course = result[0]
url = result[1]
# print(course,'---------',len(course),'-----------',len(url))
mysql_insert(course,url,config_python)
