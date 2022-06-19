from django.shortcuts import render, redirect
from .sql import get_ccgp
# Create your views here.
from .utils.form import ccgpModelForm
from .utils.pagination import Pagination
from app import models
from mysite.tools import get_domain_url


def index(request):
    return render(request, "index.html")


# 数据转化
def data(request):
    if request.method == "GET":
        return render(request, "data.html")
    d = request.POST.get("change")
    if d == "1":
        infos = get_ccgp()
        for info in infos:
            # 修改一下info，然后传进去就行了
            print(info.get("title"))
            link = info.get("link")
            domain, url = get_domain_url(link)
            info["link"] = url
            info["domain"] = domain
            form = ccgpModelForm(data=info)
            if form.is_valid():
                form.save()
    return render(request, "data.html")


def ccgp_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["title__contains"] = search_data

    queryset = models.ccgp.objects.filter(**data_dict).order_by("-publish_time")

    # context = {
    #     "search_data": search_data,

    # queryset = models.ccgp.objects.all()
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'ccgp_list.html', context)


def ccgp_add(request):
    if request.method == "GET":
        form = ccgpModelForm()
        # test = request.GET.get("test")
        # # form.instance.
        # if test:
        #     print(test)
        #     return render(request, 'ccgp_add.html', {"form": form})

        return render(request, 'ccgp_add.html', {"form": form})
    form = ccgpModelForm(data=request.POST)
    if form.is_valid():
        # 暂不保存用户提交的数据
        # form.save()
        return redirect('/ccgp/list/')
    return render(request, 'ccgp_add.html', {"form": form})
