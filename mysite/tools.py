from pathlib import Path
import json
import platform


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
