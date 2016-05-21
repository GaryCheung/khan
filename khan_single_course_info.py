from bs4 import BeautifulSoup
import requests
import pymysql
from datetime import date,datetime

course = '金融学'

def delete_today_data(config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM khanserie WHERE date = '%s'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_course_url(course,config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 查询课程url
            cursor.execute("SELECT url FROM khan WHERE course like %s" , course)
            result = cursor.fetchone()
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    return result


def get_course_detail(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    series = soup.select('table.m-clist > tr > td.u-ctitle > a')
    serie = []
    for serie_trans in series:
        serie.append(serie_trans.get_text())
    result = serie[10:len(serie)]
    return result


def mysql_insert(serie,course,config):
    for i in range(1,len(serie)):
        connection = pymysql.connect(**config)
        try:
            with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'INSERT INTO khanserie (date, serie, course) VALUES (%s, %s, %s)'
                cursor.execute(sql, (present_date, serie[i], course))
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
url = get_course_url(course , config_python)
serie = get_course_detail(url[0])
mysql_insert(serie,course,config_python)



