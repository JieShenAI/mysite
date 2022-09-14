"""
json数据的后端交互
"""
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pathlib import Path
from django.http import JsonResponse
from http import HTTPStatus
import simplejson


def get_file_json_by_fid(fid, test=False):
    s = f"app/static/json/papers/{fid}.json"  # 网站使用
    if test:
        s = f"../static/json/papers/{fid}.json"  # 测试专用
    print(Path(s).absolute())
    p = Path(s).read_text(encoding="utf-8")
    if len(p) == 0:
        p = "{}"
    return json.loads(p)


def write_file_json_by_id(fid, data, test=False):
    s = f"app/static/json/papers/{fid}.json"  # 网站使用
    if test:
        s = f"../static/json/papers/{fid}.json"  # 测试专用
    json_str = json.dumps(data)
    Path(s).write_text(json_str)


@csrf_exempt
def save_paper(request):
    """
    通过ajax提交数据
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        # print(data)
        fid = data.get('fid')
        if not fid:
            return "not found fid"
        json_data = get_file_json_by_fid(fid)
        # 先拿到文件的json数据，准备进行写入
        for key in data:
            if key == "fid":
                continue
            json_data[key] = data[key]

        # 写入文件
        write_file_json_by_id(fid, json_data)
        return JsonResponse(json_data)
    else:
        return HttpResponse("not found post")


def demo(request):
    return render(request, "1.html")


@csrf_exempt
def save_by_fid(request):
    """
    保存内容,给予成功和失败的状态码
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        fid = data.get('fid')
        if not fid:
            return HttpResponse("缺少fid参数", status=406)
        json_data = get_file_json_by_fid(fid)
        # 先拿到文件的json数据，准备进行写入
        for key in data:
            if key == "fid":
                continue
            json_data[key] = data[key]
        # 写入文件
        write_file_json_by_id(fid, json_data)
        return HttpResponse(content="200", status=200)
    else:
        return HttpResponse("只接受POST传参", status=406)


@csrf_exempt
def save_json_by_fid(request):
    """
    保存内容,给予成功和失败的状态码
    :param request:
    :return:
    """
    if request.method == "POST":
        data = simplejson.loads(request.body)
        fid = data.get('fid')
        if not fid:
            return HttpResponse("缺少fid参数", status=406)
        json_data = get_file_json_by_fid(fid)
        # 先拿到文件的json数据，准备进行写入
        for key in data:
            if key == "fid":
                continue
            json_data[key] = data[key]
        # 写入文件
        write_file_json_by_id(fid, json_data)
        return HttpResponse(content="200", status=200)
    else:
        return HttpResponse("只接受POST传参", status=406)

@csrf_exempt
def queryJson(request):
    if request.method == "POST":
        data = simplejson.loads(request.body)
        cityID = data.get("cityID")
        year = data.get("year")
        if cityID and year:
            return _getDataFromDataBase(cityID, year)
        else:
            return JsonResponse({"code": 406})
    else:
        # 以下代码，用于读取本地的json文件
        data = request.GET
        fid = data.get('fid')
        if not fid:
            return HttpResponse("缺少fid参数", status=406)
        json_data = get_file_json_by_fid(fid)
        return JsonResponse(json_data)


def _getDataFromDataBase(cityID, year):
    from mysite.tools import get_conn_cursor, free_sql
    # conn, cursor = get_conn_cursor()
    sql = "select * from vue where cityID=%s and year=%s" % (cityID, year)

    def _select(sql):
        conn, cursor = get_conn_cursor()
        res = []
        try:
            cursor.execute(sql)
            res = cursor.fetchone()
        except Exception as e:
            print(e.args)
        free_sql(conn, cursor)
        return res

    data = _select(sql)
    if not data:
        data = {}
    return JsonResponse({"code": 200, "data": data})


@csrf_exempt
def receivePaper(request):
    """
        接收前端POST传过来的数据
        保存到json文件中
    """
    if request.method == "POST":
        data = simplejson.loads(request.body)
        write_file_json_by_id("save", data)
        return HttpResponse(content="200 ok", status=200)
    else:
        return HttpResponse("只接受POST传参", status=406)


@csrf_exempt
def printPost(request):
    """
        输出POST传递过来的参数
    """
    if request.method == "POST":
        data = simplejson.loads(request.body)
        return JsonResponse(data)
    else:
        return HttpResponse("只接受post传参", status=406)


def _saveImg(ImgBase64):
    import base64
    img_data = base64.b64decode(ImgBase64)
    with open("./test.png", "wb") as f:
        f.write(img_data)
        f.close()


if __name__ == '__main__':
    data = get_file_json_by_fid("enshi", test=True)
    # write_file_json_by_id(2, data)
    print(data)
