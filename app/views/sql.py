from app.models import ccgp
from django.shortcuts import render, redirect, HttpResponse
from django.db import connection


def test(request):
    sql_str = "SELECT announce_type , COUNT(*) FROM app_ccgp WHERE DATE(publish_time) = DATE_SUB(CURDATE(),INTERVAL 1 DAY) GROUP BY announce_type;"
    # sql_str = "select * FROM app_ccgp limit 5"
    sql_data = ccgp.objects.raw(sql_str)
    for _ in sql_data:
        print(_)
    return HttpResponse("ok")


delta_day = "WHERE  TO_DAYS(NOW()) - TO_DAYS(publish_time) = %s "


def my_custom_sql(request):
    with connection.cursor() as cursor:
        sql_str = f"SELECT announce_type , COUNT(*) FROM app_ccgp {delta_day} GROUP BY announce_type;"
        # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        # cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        cursor.execute(sql_str, [2])
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    return HttpResponse("ok")
