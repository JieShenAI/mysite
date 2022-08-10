
from io import StringIO
from django.shortcuts import render, redirect, HttpResponse
import json
from pathlib import Path
from django.http import JsonResponse
from http import HTTPStatus
from app.views.jsons import get_file_json_by_fid
import os
from django.http import Http404, StreamingHttpResponse, FileResponse
"""
文件相关的操作：
    下载规划word文档
"""


headContent = []  # for dfs()


def dfs(content: dict, level=1):
    """
    递归依序排列标题和段落
    """
    for key in content.keys():
        if type(content.get(key)) == dict:
            headContent.append((key, "", level))
            dfs(content.get(key), level+1)
        else:
            headContent.append((key, content.get(key), level))


def paperFileDown(filename, firsthead):
    from docx import Document
    document = Document()

    document.add_heading(firsthead, level=0)
    for head, paragraph, level in headContent:
        document.add_heading(head, level=level)
        document.add_paragraph(paragraph)

    fileLocation = os.path.join("down", filename)
    document.save(fileLocation)
    try:
        response = FileResponse(open(fileLocation, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + \
            os.path.basename(filename)
        return response
    except Exception:
        raise Http404


def paperDown(request):
    if request.method == "GET":
        data = request.GET
        fid = data.get("fid")
        json_data = get_file_json_by_fid(fid)

        # 按序增加标题和段落
        dfs(json_data)
        firsthead = data.get("firsthead") if data.get("firsthead") else "规划"
        # 文件名
        import time
        filename = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".docx"
        response = paperFileDown(filename, firsthead)
        return response
