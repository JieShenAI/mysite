from app import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app.utils.bootstrap import BootStrapModelForm
from django import forms

# class HostModelForm(BootStrapModelForm):
#     # domain = forms.CharField(
#     #     label="域名",
#     #     validators=[RegexValidator(r'^1[3-9]\d{9}$', 'xxx错误'), ],
#     # )
#
#     class Meta:
#         model = models.Host
#         fields = "__all__"
#
#     # 验证：方式2
#     def clean_domain(self):
#         # 当前编辑的哪一行的ID
#         # print(self.instance.pk)
#         txt_domain = self.cleaned_data["domain"]
#         print(txt_domain)
#         # exists = models.Host.objects.exclude(id=self.instance.pk).filter(domain=txt_domain).exists()
#         exists = models.Host.objects.filter(domain=txt_domain).exists()
#         if exists:
#             raise ValidationError("域名已存在")
#
#         # 验证通过，用户输入的值返回
#         return txt_domain


# class UserModelForm(BootStrapModelForm):
#     name = forms.CharField(
#         min_length=3,
#         label="用户名",
#         widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#
#     class Meta:
#         model = models.UserInfo
#         fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
from app.utils.encrypt import md5


# class UserModelForm(BootStrapModelForm):
#     class Meta:
#         model = models.users
#         fields = "__all__"
#         exclude = ['status', 'level']


class UserRegisterModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.users
        fields = ["email", "username", 'password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        # 注册用户，无需比对之前的密码，留到修改密码
        # 去数据库校验当前密码和新输入的密码是否一致
        # exists = models.users.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        # if exists:
        #     raise ValidationError("不能与以前的密码相同")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm


class ccgpModelForm(BootStrapModelForm):
    class Meta:
        model = models.ccgp
        fields = "__all__"

    # # 验证：方式2
    # def clean_link(self):
    #     # 当前编辑的哪一行的ID
    #     # print(self.instance.pk)
    #     txt = self.cleaned_data["link"]
    #     # exists = models.Host.objects.exclude(id=self.instance.pk).filter(domain=txt_domain).exists()
    #     exists = models.Host.objects.filter(domain=txt).exists()
    #     if exists:
    #         raise ValidationError("已存在")
    #
    #     # 验证通过，用户输入的值返回
    #     return txt

    def clean_title(self):
        raise ValidationError("暂不开放此功能，您输入的数据不会被保存")
