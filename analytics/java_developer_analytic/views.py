from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import *


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
    set_list = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    data = {}
    for i, year in enumerate(set_list):
        data["year" + str(i)] = year
        skill_by_year = Skills.objects.filter(year=year)
        for j in range(10):
            data["skill" + str(i) + "_" + str(j)] = skill_by_year[j].skill
            data["count" + str(i) + "_" + str(j)] = skill_by_year[j].skill_count
    return render(request, "skills.html", context=data)


def latest_vacancies(request):
    return render(request, "latest-vacancies.html")
