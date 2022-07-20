
from datetime import datetime, date, timedelta
import pymysql
import pandas as pd

# ---------连接--------------
connect = pymysql.connect(host='cdb-o80nxgle.bj.tencentcdb.com',   # ip
                          port=10229,                              # 端口
                          user='shenjie',
                          password='f#8#7@@JfSD',
                          db='BiddingNetwork',
                          charset='utf8') #服务器名,账户,密码，数据库名称
cursor = connect.cursor()

#timetoday = datetime.date.today()  获取当前日期

timetoday = date.today() + timedelta(days = -1) 
Btimetoday = date.today() + timedelta() 
Qtimetoday = date.today() + timedelta(days = -7) 
todaytime_str = timetoday.strftime('%Y-%m-%d')
time_str = Btimetoday.strftime('%Y-%m-%d')
Qtime_str = Qtimetoday.strftime('%Y-%m-%d')

Title = ['公告名称', '采购人信息', '代理机构','公告类型', '所属地区', 'link1', 'link2','公告时间']

#获取前日总数
cursor.execute("select count(announce_type) from app_ccgp where publish_time like binary '%s'" % ('%s%%' % timetoday))
print("昨日更新公告数为:%s" % cursor.fetchone())

#nums = str(cursor.fetchall())
#print('昨日更新公告数为',nums)


#获取公告类型分类组合
cursor.execute("select announce_type ,count(announce_type) from app_ccgp where publish_time like binary '%s'  Group BY announce_type" % ('%s%%' % timetoday))
Typedata = list(cursor.fetchall())
Typeframe = pd.DataFrame(Typedata)


##获取地区分类组合
cursor.execute("select province ,count(province) from app_ccgp where publish_time like binary '%s'  Group BY province" % ('%s%%' % timetoday))
Citydata = list(cursor.fetchall())
Cityframe = pd.DataFrame(Citydata)


##获取前一天数据
cursor.execute("select title,purchaser,agency,announce_type,province,domain,link,publish_time from app_ccgp where publish_time like binary '%s' order by (announce_type) " % ('%s%%' % timetoday))
Daydata = list(cursor.fetchall())
#Dayframe = pd.DataFrame(data=Daydata,

Dayframe = pd.DataFrame(data=Daydata,columns =Title)


##获取一周内数据  

Qsql='SELECT title,purchaser,agency,announce_type,province,domain,link,publish_time FROM app_ccgp where publish_time Between '+ "'"+ Qtime_str+ "'"+' And '+ "'"+time_str+ "'"+ 'order by (publish_time)'

cursor.execute(Qsql)
QDaydata = list(cursor.fetchall())
QDayframe = pd.DataFrame(data=QDaydata,columns =Title)

name='Typeframe'+  todaytime_str + '.xlsx'
with pd.ExcelWriter(
    name,
    datetime_format='YYYY-MM-DD'  # 只显示年月日, 不显示时分秒
) as writer:
    Typeframe.to_excel(writer, sheet_name='公告类型')  # Sheet1
    Cityframe.to_excel(writer, sheet_name='不同城市')  # Sheet2
    Dayframe.to_excel(writer, sheet_name='一天数据')   # Sheet3
    QDayframe.to_excel(writer, sheet_name='一周内数据')   # Sheet4


cursor.close()
print('运行成功……')









"""
python中数据库中like用法-----------------
sql1 = "SELECT * FROM T_SECTION WHERE TITLE LIKE '%%%%%s%%%%'" % sel
#SELECT * FROM T_SECTION WHERE TITLE LIKE '%%name%%'

#print(Qsql)  QDayframe.to_excel('list.xlsx', '公告类型', index=False)

"""