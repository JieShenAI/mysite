import pymysql
from pathlib import Path
import json
import platform

"""
    外部导包方式参考：
        from mysite.tools import load_sql_info,...
"""


def load_sql_info(filename):
    """
    mysite.json
    :param filename:
    :return:
    """
    p = Path()
    p = p.home().joinpath(".jiejie/mysql").joinpath(filename)
    return json.loads(p.read_text())


def get_domain_url(link: str):
    """
    url = "http://127.0.0.1/21/12"
    :param link:
    :return:
    """
    from urllib.parse import urlparse
    domain = urlparse(link).netloc
    start = link.index(domain) + len(domain)
    return domain, link[start::]


def load_static():
    _ = Path().home().joinpath(".jiejie/statics")
    if platform.system().lower() == 'windows':
        p = _.joinpath("win.json")
    elif platform.system().lower() == 'linux':
        p = _.joinpath("linux.json")
    # 其他平台 ，暂不支持，直接报错 Permission denied
    return json.loads(p.read_text())


# 数据库连接配置与连接池
def _get_cursor(host, port, user, sql_pwd, db):
    conn = pymysql.connect(host=host, port=port,
                           user=user, passwd=sql_pwd, charset='utf8', db=db)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, cursor


def get_conn_cursor():
    sql_json = load_sql_info("sql_v5.json")
    db = sql_json.get("db")
    user = sql_json.get("user")
    sql_pwd = sql_json.get("pwd")
    port = sql_json.get("port")
    host = sql_json.get("host")
    return _get_cursor(host, port, user, sql_pwd, db)


def free_sql(conn, cursor):
    """
        释放数据库连接
    """
    try:
        cursor.close()
    except Exception as e:
        print(e.args)
    try:
        conn.close()
    except Exception as e:
        print(e.args)
