from app.models import ccgp
from django.shortcuts import render, redirect, HttpResponse
from pathlib import Path
import json
from django.http import JsonResponse


def nianjian(request):
    return render(request, "nianjian.html")


def getInfoByID(request):
    """
    eg:
        http://127.0.0.1:8000/data/areainfo?year=2020&areaID=420100
    通过年份，区域ID获得该地区在数据库中所存储的信息
    :param request:
    :return:
    """
    if request.method == "GET":
        data = request.GET
        year = data['year']
        areaID = data['areaID']
        head_filepath = f"app/static/json/{year}/"
        if areaID[2::] == "0000":
            filepath = head_filepath + "province.json"
        else:
            filepath = head_filepath + areaID[:2:] + ".json"
        try:
            json_str = Path(filepath).read_text()
            json_data = json.loads(json_str)
            txt = {}
            # 读入属性名
            enZh = "app/static/json/sql/EnZh.json"
            enZh_str = Path(enZh).read_text()
            enZh_json_data = json.loads(enZh_str)
            for key in json_data[areaID]:
                txt[enZh_json_data[key]] = json_data[areaID][key]
        except:
            txt = {}
        return JsonResponse(txt)

