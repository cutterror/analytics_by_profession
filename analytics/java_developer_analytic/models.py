from django.db import models


class Demand(models.Model):
    year = models.IntegerField()
    average_salary = models.IntegerField()
    vacancy_num = models.IntegerField()
    selected_average_salary = models.IntegerField()
    selected_vacancy_num = models.IntegerField()

    class Meta:
        verbose_name = 'востребованность'


class GeographyPercent(models.Model):
    city = models.CharField(max_length=100)
    percent_vacancy_num = models.IntegerField()

    class Meta:
        verbose_name = 'география-количество-вакансий'


class GeographySalary(models.Model):
    city = models.CharField(max_length=100)
    average_salary = models.IntegerField()

    class Meta:
        verbose_name = 'география-зарплаты'


class Skills(models.Model):
    skill = models.CharField(max_length=100)
    skill_count = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        verbose_name = 'навыки'
