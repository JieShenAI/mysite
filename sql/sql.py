import json
import pymysql
from pathlib import Path

# ---------连接--------------
connect = pymysql.connect(host='cdb-o80nxgle.bj.tencentcdb.com',  # ip
                          port=10229,  # 端口
                          user='shenjie',
                          password='f#8#7@@JfSD',
                          db='Anshan_Database',
                          charset='utf8')  # 服务器名,账户,密码，数据库名称
cursor = connect.cursor()

sql_str = "SELECT  * FROM Statistical_Yearbook;"

cursor.execute(sql_str)
rows = cursor.fetchall()
print(len(rows))

fields_tmp = cursor.description
fields = [_[0] for _ in fields_tmp]
fields = fields[1::]
fields = fields[:-3:]
content = {}


for data in rows:
    data = data[1::]
    data = data[:-3:]
    row = dict(zip(fields, data))
    for k in row.keys():
        row[k] = str(row[k])
    # 年份
    year = int(row["STATISTICAL_YEAR"])
    # 省份 ADMINISTRATIVE_CODE
    city_code = str(row["ADMINISTRATIVE_CODE"])
    province = city_code[:2:]
    if year not in content:
        content[year] = {}
    if province not in content[year]:
        content[year][province] = {}

    # 'PROVINCE': '安徽省', 'CITY': '', 'COUNTY': '', 'STATISTICAL_YEAR': 1999,
    delete_attr = ['PROVINCE', 'CITY', 'COUNTY', 'STATISTICAL_YEAR', 'FORMER_NAME']

    for k in row.keys():
        if row[k] is None or row[k] == 'None':
            delete_attr.append(k)
    for attr in delete_attr:
        del row[attr]
    content[year][province][city_code] = row


for year in content.keys():
    print(year)
    province_json = {}
    for province in content[year].keys():
        print(province)
        v = content[year][province]
        print("len: ", len(v))
        print(Path(".").joinpath("../app/static/json/%s/%s.json" % (year, province)))
        print()
        json_data = json.dumps(v)
        p = Path(".").joinpath("../app/static/json/%s" % year)
        p.mkdir(exist_ok=True)
        p.joinpath("%s.json" % province).write_text(json_data)

