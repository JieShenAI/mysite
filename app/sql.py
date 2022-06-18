from datetime import datetime
import pymysql
from mysite.tools import load_sql_info

data = load_sql_info("ccgp.json")
ccgp_table = "ccgp"
# proxy
proxy_table = "proxy"


# 1.连接MySQL


def get_cursor():
    conn = pymysql.connect(host=data.get("host"), port=data.get("port"),
                           user=data.get("user"), passwd=data.get("pwd"), charset='utf8', db=data.get("db"))
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, cursor


def close(conn, cursor):
    try:
        cursor.close()
    except Exception as e:
        print(e.args)
    try:
        conn.close()
    except Exception as e:
        print(e.args)


def _select(sql):
    conn, cursor = get_cursor()
    res = []
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
    except Exception as e:
        print(e.args)
    close(conn, cursor)
    return list(res)


# ccgp

def ccgp_save(link=None, title=None, publish_time=None, purchaser=None, agency=None, announce_type=None, province=None,
              txt=None, map=None):
    """
    * 摘要
    ccgp_save(link, title, publish_time, purchaser, agency, announce_type, province)
    * 内容
    ccgp_save(link=,txt=,map=)
    link 是主键
    """
    """
        title = models.CharField(max_length=50)
        publish_time = models.DateTimeField()
        purchaser = models.CharField(max_length=50)
        agency = models.CharField(max_length=50)
        announce_type = models.CharField(max_length=10)
        province = models.CharField(max_length=10)
        link = models.CharField(max_length=100,primary_key=True)
        txt = models.TextField()
        map = models.TextField()
    """
    conn, cursor = get_cursor()
    if link is None:
        return False
    if txt is None and map is None:
        # 插入摘要部分
        sql = f"insert into {ccgp_table}(title,publish_time,purchaser,agency,announce_type,province,link,txt,map) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (title, publish_time, purchaser,
                                 agency, announce_type, province, link, "", ""))
            conn.commit()
        except Exception as e:
            # print(e.args)
            close(conn, cursor)
            return False
        close(conn, cursor)
        return True
    sql = f"update {ccgp_table} set txt=%s,map=%s where link='{link}'"
    if txt is not None and map is not None:
        try:
            cursor.execute(sql, (txt, map))
            conn.commit()
        except Exception as e:
            # print(e.args)
            close(conn, cursor)
            return False
        close(conn, cursor)
        return True
    close(conn, cursor)
    return False


# def ccgp_purchase_insert(purchase: Purchase):
#     return ccgp_save(
#         link=purchase.link,
#         title=purchase.title,
#         publish_time=purchase.publish_time,
#         purchaser=purchase.purchaser,
#         agency=purchase.agency,
#         announce_type=purchase.announce_type,
#         province=purchase.province
#     )


def update_ccgp_txt_map(link, txt, map):
    return ccgp_save(link=link, txt=txt, map=map)


def get_ccgp_txt_map_is_null() -> list:
    sql = f"SELECT * FROM {ccgp_table} WHERE txt='' OR map='';"
    return _select(sql)


def get_ccgp() -> list:
    sql = f"SELECT * FROM {ccgp_table};"
    return _select(sql)


"""
记录所有的代理ip,记录每个代理ip的存活状态
"""


# 数据存入数据库

def proxy_insert(ip: str = None, port=None, alive: bool = False) -> bool:
    """
    # 插入新代理
    proxy_save(ip, port, alive)

    * ip
    * port
    * alive
    * last_alive_date : 该代理上一次存活的时间，若时间过于久远，删除该代理
    """
    conn, cursor = get_cursor()
    if ip is not None and port is not None:
        try:
            sql = f"insert into {proxy_table}(ip,port,alive,last_alive_date) values(%s,%s,%s,%s)"
            cursor.execute(sql, (ip, port, alive, datetime.now()))
            conn.commit()
        except Exception as e:
            # 暂不考虑，代理ip更换port导致插入失败的情况
            # print(e.args)
            close(conn, cursor)
            return False
        close(conn, cursor)
        return True
    close(conn, cursor)
    return False


def proxy_update(ip: str = None, alive: bool = False):
    """
        修改代理存活状态
    """
    conn, cursor = get_cursor()
    if alive is True:
        sql = f"update {proxy_table} set alive = %s,last_alive_date='{datetime.now()}' where ip=%s"
    else:
        sql = f"update {proxy_table} set alive = %s where ip=%s"
    try:
        cursor.execute(sql, (alive, ip))
        conn.commit()
    except:
        close(conn, cursor)
        return False
    close(conn, cursor)
    return True


def proxy_delete(ip: str) -> bool:
    """
        代理ip，死亡后，将其从数据库删除
    """
    conn, cursor = get_cursor()
    sql = f"DELETE FROM {proxy_table} WHERE ip=%s"
    try:
        cursor.execute(sql, ip)
        conn.commit()
    except:
        close(conn, cursor)
        return False
    close(conn, cursor)
    return True


def get_proxy_all() -> list:
    sql = f"select * from {proxy_table}"
    return _select(sql)


# 在主程序退出的时候，记得关闭
# cursor.close()
# conn.close()
if __name__ == '__main__':
    v = get_ccgp_txt_map_is_null()
    print(v)
