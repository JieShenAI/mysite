from django.shortcuts import render, redirect
from app.utils.pagination import Pagination
from app import models

from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from app.utils.code import check_code
from app import models
from app.utils.bootstrap import BootStrapForm
from app.utils.encrypt import md5
from app.utils.form import UserRegisterModelForm


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # {'username': 'wupeiqi', 'password': '123',"code":123}
        # {'username': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f',"code":xxx}

        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # user_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        user_object = models.users.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        if user_object.status == 0:
            form.add_error("username", "您已完成注册，请等待管理员审核")
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_object.id, 'name': user_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/")

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')


def register(request):
    if request.method == "GET":
        form = UserRegisterModelForm()
        return render(request, "register.html", {"form": form})
    form = UserRegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login/')
    form = UserRegisterModelForm(data=request.POST)
    # form.add_error("email", "拒绝注册")
    # form.add_error("username", "拒绝注册")
    if form.is_valid():
        # 先不允许注册
        form.save()
        return redirect('/login/')
    return render(request, "register.html", {"form": form})

# def admin_reset(request, nid):
#     """ 重置密码 """
#     # 对象 / None
#     row_object = models.Admin.objects.filter(id=nid).first()
#     if not row_object:
#         return redirect('/admin/list/')
#
#     title = "重置密码 - {}".format(row_object.username)
#
#     if request.method == "GET":
#         form = AdminResetModelForm()
#         return render(request, 'change.html', {"form": form, "title": title})
#
#     form = AdminResetModelForm(data=request.POST, instance=row_object)
#     if form.is_valid():
#         form.save()
#         return redirect('/admin/list/')
#     return render(request, 'change.html', {"form": form, "title": title})

# def pretty_add(request):
#     """ 添加靓号 """
#     if request.method == "GET":
#         form = PrettyModelForm()
#         return render(request, 'pretty_add.html', {"form": form})
#     form = PrettyModelForm(data=request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect('/pretty/list/')
#     return render(request, 'pretty_add.html', {"form": form})
