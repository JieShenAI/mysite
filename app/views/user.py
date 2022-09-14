from django.shortcuts import render, redirect, HttpResponse
from app.utils.token import create_token, check_token
from django.views.decorators.csrf import csrf_exempt
import simplejson
from django.http.response import JsonResponse

from mysite.tools import get_conn_cursor, free_sql


def login(request):
    """
        当前只要账号和密码正确就允许访问
            为了简单起见
    """
    pass


@csrf_exempt
def register(request):
    """
        提供邮箱，邀请码，(暂不提供发送邮件的功能)
        用户名，邮箱账号，密码(md5)，邀请码(邮箱验证码)，status,level，查询出是否有该用户
    """
    if request.method == "POST":
        data = simplejson.loads(request.body)
        username = data.get("username")  # 唯一
        email = data.get("email")  # 唯一
        pwd_md5 = data.get("password")
        code = data.get("code")
        if code == "Zds9gHfgf88":
            return JsonResponse(_add_user(username, email, pwd_md5))
    return JsonResponse({"code": 500})


def _add_user(username, email, pwd_md5):
    conn, cursor = get_conn_cursor()
    res_obj = {}
    # sql = "INSERT INTO users(username,email,pwd_md5) VALUES(%s,%s,%s);" % (username, email, pwd_md5)
    sql = f"INSERT INTO users(username,email,pwd_md5) VALUES('{username}','{email}','{pwd_md5}');"
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
        res_obj["code"] = 200
    except Exception as e:
        res_obj["code"] = 500
        print(e.args)
    free_sql(conn, cursor)
    return res_obj


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = simplejson.loads(request.body)
        name_email = data.get("name_email")
        pwd_md5 = data.get("password")
        username = _select_user(name_email, pwd_md5)
        _token = create_token(username)
        # 先查询是否有该用户
        if username != "":
            return JsonResponse({"code": 200, "data": {"token": _token, "nickName": username}})
        else:
            return JsonResponse({"code": 500})
    else:
        JsonResponse({"code": 406, "data": {"msg": "reject get"}})

def _select_user(name_email, pwd_md5):
    conn, cursor = get_conn_cursor()
    sql = 'SELECT username FROM users WHERE (username = "%s" OR email="%s") AND pwd_md5 = "%s"' % (
        name_email, name_email, pwd_md5)
    username = ""
    try:
        cursor.execute(sql)
        one = cursor.fetchone()
        if one is None:
            return ""
        username = list(one.values())[0]
    except Exception as e:
        print(e.args)
    free_sql(conn, cursor)
    return username
