from pathlib import Path
import json


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

