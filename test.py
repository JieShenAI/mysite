import os
import sys
from app import models
import django

if __name__ == "__main__":
    # test1是我的主应用名字
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    first = models.ccgp.objects.first()
    print(first)
