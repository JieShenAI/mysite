from app import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app.utils.bootstrap import BootStrapModelForm


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
