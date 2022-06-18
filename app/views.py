from django.shortcuts import render, redirect
from .sql import get_ccgp
# Create your views here.
from .utils.form import HostModelForm, ccgpModelForm
from .utils.pagination import Pagination
from app import models


def index(request):
    return render(request, "index.html")


# 数据转化
def data(request):
    if request.method == "GET":
        return render(request, "data.html")
    d = request.POST.get("change")
    if d == "1":
        infos = get_ccgp()
        # print(*infos[::3], sep="/n")
        for info in infos:
            # 修改一下info，然后传进去就行了
            link = info.get("link")
            # django 有外键约束的值，怎么插入
            models.ccgp.objects.create(info)
    return render(request, "data.html")


def domain_list(request):
    queryset = models.Host.objects.all()
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'domain_list.html', context)


def domain_add(request):
    if request.method == "GET":
        form = HostModelForm()
        return render(request, 'domain_add.html', {"form": form})
    form = HostModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/domain/list/')
    return render(request, 'domain_add.html', {"form": form})


def ccgp_list(request):
    queryset = models.ccgp.objects.all()
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'ccgp_list.html', context)


def ccgp_add(request):
    if request.method == "GET":
        test = request.GET.get("test")
        form = ccgpModelForm()
        # form.instance.
        if test:
            print(test)
            return render(request, 'ccgp_add.html', {"form": form})

        return render(request, 'ccgp_add.html', {"form": form})
    form = ccgpModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/ccgp/list/')
    return render(request, 'ccgp_add.html', {"form": form})
