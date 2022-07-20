from app.models import ccgp
from django.shortcuts import render, redirect, HttpResponse


def nianjian(request):
    return render(request,"nianjian.html")
