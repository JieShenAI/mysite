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
    # 确实有名称重复的公告
    title = models.TextField(verbose_name="标题")
    purchaser = models.CharField(verbose_name="采购人", default="", max_length=50)
    agency = models.CharField(verbose_name="代理机构", default="", max_length=50)
    announce_type = models.CharField(verbose_name="公告类型", default="", max_length=10)
    # 有的没有省份
    province = models.CharField(verbose_name="省份", default=None, max_length=10, null=True, blank=True)
    txt = models.TextField(verbose_name="文本", default="")
    map = models.TextField(verbose_name="公告概要", default="")
    link = models.CharField(verbose_name="链接", max_length=100, unique=True)
    domain = models.CharField(verbose_name="域名", max_length=30)


class users(models.Model):
    email = models.CharField(verbose_name="邮箱", max_length=30, unique=True)
    username = models.CharField(verbose_name="用户名", max_length=32, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    status_choices = (
        (0, "停用"),
        (1, "正常")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)
    level_choices = (
        (1, "正常用户"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)

    # 暂不引入部门
    def __str__(self):
        return self.username

# class proxy(models.Model):
#     """
#     """
#     ip = models.CharField(max_length=15,primary_key=True)
#     port = models.IntegerField()
#     alive = models.BooleanField()
#     alive_date = models.DateTimeField(auto_now=True)
