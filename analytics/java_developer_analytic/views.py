from django.contrib.sites import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json


def index(request):
    return render(request, "index.html")


def demand(request):
    return render(request, "demand.html")


def geography(request):
    return render(request, "geography.html")


def skills(request):
    return render(request, "skills.html")


def latest_vacancies(request):
    return render(request, "latest-vacancies.html")


# def get_vacancies(request):
#     if request.method == 'GET':
#         pass
