from django.shortcuts import render
from .models import *
from .hhApi.hh_vacancies import HHJavaVacancies
import re


def index(request):
    return render(request, "index.html")


def demand(request):
    demand_table = Demand.objects.all()
    data = {}
    for i in range(len(demand_table)):
        data["year" + str(i)] = demand_table[i].year
        data["salary" + str(i)] = demand_table[i].average_salary
        data["num" + str(i)] = demand_table[i].vacancy_num
        data["salary_sel" + str(i)] = demand_table[i].selected_average_salary
        data["num_sel" + str(i)] = demand_table[i].selected_vacancy_num
    return render(request, "demand.html", context=data)


def geography(request):
    city_salary = GeographySalary.objects.all()
    city_percent = GeographyPercent.objects.all()
    data = {}
    for i in range(len(city_salary)):
        data["city" + str(i)] = city_salary[i].city
        data["salary" + str(i)] = city_salary[i].average_salary
        data["city_per" + str(i)] = city_percent[i].city
        data["percent" + str(i)] = city_percent[i].percent_vacancy_num
    return render(request, "geography.html", context=data)


def skills(request):
    years = sorted(list(set([value.year for value in Skills.objects.all()])))
    data = {}
    for i, year in enumerate(years):
        data["year" + str(i)] = year
        skill_by_year = Skills.objects.filter(year=year)
        for j in range(10):
            data["skill" + str(i) + "_" + str(j)] = skill_by_year[j].skill
            data["count" + str(i) + "_" + str(j)] = skill_by_year[j].skill_count
    return render(request, "skills.html", context=data)


def get_salary_str(vacancy: dict):
    if vacancy["salary"] is None:
        return "Не указан"
    elif vacancy["salary"]["from"] is None and vacancy["salary"]["to"] is not None:
        return f'до {vacancy["salary"]["to"]}'
    elif vacancy["salary"]["to"] is None and vacancy["salary"]["from"] is not None:
        return f'от {vacancy["salary"]["from"]}'
    return f'{vacancy["salary"]["from"]} - {vacancy["salary"]["to"]}'


def clean_string(string: str):
    result = re.sub(re.compile('<.*?>'), '', string).split("\n")
    return ", ".join([" ".join(value.strip().split()) for value in result])


def latest_vacancies(request):
    java_vacancies = HHJavaVacancies().vacancies
    data = {}
    for i, vacancy in enumerate(java_vacancies):
        data["name" + str(i)] = vacancy["name"]
        data["description" + str(i)] = "Не указано" if vacancy["snippet"]["responsibility"] is None \
            else clean_string(vacancy["snippet"]["responsibility"])
        data["skills" + str(i)] = "Не указаны" if vacancy["snippet"]["requirement"] is None \
            else clean_string(vacancy["snippet"]["requirement"])
        data["salary" + str(i)] = get_salary_str(vacancy)
        data["city" + str(i)] = vacancy["area"]["name"]
        data["company" + str(i)] = vacancy["employer"]["name"]
        data["date" + str(i)] = vacancy["published_at"][:10]
    return render(request, "latest-vacancies.html", context=data)
