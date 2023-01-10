from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Главная")


def demand(request):
    return HttpResponse("Востребованность")


def geography(request):
    return HttpResponse("География")


def skills(request):
    return HttpResponse("Навыки")


def latest_vacancies(request):
    return HttpResponse("Последние вакансии")
