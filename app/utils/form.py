from app import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app.utils.bootstrap import BootStrapModelForm


class DomainModelForm(BootStrapModelForm):
    # domain = forms.CharField(
    #     label="域名",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', 'xxx错误'), ],
    # )

    class Meta:
        domain = models.Host
        fields = "__all__"

    # 验证：方式2
    # def clean_mobile(self):
    #     # 当前编辑的哪一行的ID
    #     # print(self.instance.pk)
    #     txt_domain = self.cleaned_data["domain"]
    #     # exists = models.Host.objects.exclude(id=self.instance.pk).filter(domain=txt_domain).exists()
    #     exists = models.Host.objects.filter(domain=txt_domain).exists()
    #     if exists:
    #         raise ValidationError("域名已存在")
    #
    #     # 验证通过，用户输入的值返回
    #     return txt_domain
