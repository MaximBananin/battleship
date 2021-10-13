# from django.http import HttpResponse
from django.shortcuts import render


def main_view(request, room):
    return render(request,'game/index.html')
