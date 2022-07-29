from django.shortcuts import render, redirect, HttpResponse


def show_paper(request):
    return render(request, "paper.html")


def chooseArea(request):
    return render(request, "chooseArea.html")


def paperAnalysis(request):
    return render(request, "struct.html")
