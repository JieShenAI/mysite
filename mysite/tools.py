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
