
from io import StringIO
from django.shortcuts import render, redirect, HttpResponse
import json
from pathlib import Path
from django.http import JsonResponse
from http import HTTPStatus

# TODO 上线记得开启
from app.views.jsons import _saveImg, get_file_json_by_fid

import os
from django.http import Http404, StreamingHttpResponse, FileResponse
from docx import Document

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


""""
以下是Vue的文档导出
"""


def downWord(request):
    autoGenerateWord("enshi", "save")
    fileLocation = "./test.docx"
    try:
        response = FileResponse(open(fileLocation, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + \
            os.path.basename(fileLocation)
        return response
    except Exception:
        raise Http404


def autoGenerateWord(structJson, textJson):
    """
        structJson: 
            eg: enshi
            文章标题的json文件
        textJson:
            eg: save
            前端传到后端的json文件
    """
    # from jsons import get_file_json_by_fid  本地测试
    js = get_file_json_by_fid(structJson)
    up_json = get_file_json_by_fid(textJson)

    document = Document()
    document.add_heading(js["title"], level=0)
    document.add_heading(js["subtitle"], level=0)

    for chapter in js["content"]:
        """
        js["content"] 为

        {
            'ch1': {
                'se1' : [{'h1': 'content1'}, {'textarea': 'contnt2'}]
            }
        }
        """
        ch_key, ses = list(chapter.items())[0]
        for se_key in ses.keys():
            content = ses[se_key]
            # 获取前端传过来的输入款的数据
            textarea_arr = list(up_json[ch_key][se_key]["txts"].values())
            if up_json[ch_key][se_key].get("imgs"):
                img_dict = up_json[ch_key][se_key]["imgs"]
            else:
                img_dict = []
            t = 0
            img_idx = 1
            for element in content:
                ele_key, ele_value = list(element.items())[0]
                if len(ele_key) == 2 and ele_key[0] == "h":
                    lv = int(ele_key[1])
                    document.add_heading(ele_value, level=lv)
                elif ele_key == "textarea":
                    document.add_paragraph(
                        textarea_arr[t:t+1:][0] if textarea_arr[t:t+1:] else ""
                    )
                    t += 1
                elif ele_key == "img":
                    k = "img"+str(img_idx)
                    if k in img_dict.keys():
                        _saveImg(img_dict.get(k))
                        img_idx += 1
                        picture = document.add_picture("./test.png")
                        picture.width = int(
                            picture.width * 0.30)  # 宽度缩放为原来的30%
                        picture.height = int(
                            picture.height * 0.30)  # 高度缩放为原来的30%

    document.save("./test.docx")


if __name__ == "__main__":
    autoGenerateWord()
