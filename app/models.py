from django.db import models


# Create your models here.

class ccgp(models.Model):
    """
    Purchase(
        title='临沂市自然资源和规划局打字复印制图编辑项目更正公告',
        time='2022.06.04 19:22:22',
        purchaser='临沂市自然资源和规划局机关',
        agency='山东诺顿项目管理有限公司',
        announce_type='更正公告',
        province='山东',
        link='http://www.ccgp.gov.cn/cggg/dfgg/gzgg/202206/t20220604_18018835.htm'
    )
    """
    publish_time = models.DateTimeField(verbose_name="发布时间")
    title = models.CharField(verbose_name="标题", max_length=50, unique=True)
    purchaser = models.CharField(verbose_name="采购人", max_length=50)
    agency = models.CharField(verbose_name="代理机构", max_length=50)
    announce_type = models.CharField(verbose_name="公告类型", max_length=10)
    province = models.CharField(verbose_name="省份", max_length=10)
    txt = models.TextField(verbose_name="文本", default="")
    map = models.TextField(verbose_name="公告概要", default="")
    link = models.CharField(verbose_name="链接", max_length=100, unique=True)
    domain = models.CharField(max_length=30)
    host = models.ForeignKey(verbose_name="host", to="Host", to_field="id", null=True, blank=True,
                             on_delete=models.SET_NULL)


class Host(models.Model):
    domain = models.CharField(verbose_name="域名", max_length=30)

    def __str__(self):
        return self.domain

# class proxy(models.Model):
#     """
#     """
#     ip = models.CharField(max_length=15,primary_key=True)
#     port = models.IntegerField()
#     alive = models.BooleanField()
#     alive_date = models.DateTimeField(auto_now=True)
