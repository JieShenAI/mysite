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


def get_file_json_by_fid(fid):
    s = f"app/static/json/papers/{fid}.json"  # 网站使用
    # s = f"../static/json/papers/{fid}.json"  # 测试专用
    # print("绝对: ", Path(s).absolute())
    p = Path(s).read_text()
    if len(p) == 0:
        p = "{}"
    return json.loads(p)


def write_file_json_by_id(fid, data):
    s = f"app/static/json/papers/{fid}.json"  # 网站使用
    # s = f"../static/json/papers/{fid}.json" # 测试专用
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


def queryJson(request):
    if request.method == "GET":
        data = request.GET
        fid = data.get('fid')
        if not fid:
            return HttpResponse("缺少fid参数", status=406)
        json_data = get_file_json_by_fid(fid)
        return JsonResponse(json_data)
    else:
        return HttpResponse("只接受get传参", status=406)


if __name__ == '__main__':
    data = get_file_json_by_fid(8888)
    # write_file_json_by_id(2, data)
    print(data)
