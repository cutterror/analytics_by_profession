import math
from vacancy import Vacancy
from year import Year
from city import City


def check_statistics_preparedness(method):
    """Декоратор для геттеров полей, инициализацию которых нужно проверить и, в случае необходимости,
       выполнить перед выдачей"""

    def wrapper(self):
        if not self.fulfillment:
            self.calculate_statistics()
        return method(self)
    return wrapper


class Statistic:
    """Класс для представления статистики по вакансиям

    Attributes:
        self.__selected_vacancy (str): Выбранное название вакансии для дополнительной статистики
        self.__vacancies_count (int): Количество вакансий
        self.__cities (dict): Словарь, где ключ - название города, а значение - соответсвующий ему объект City
        self.__years (dict): Словарь, где ключ - год, а значение - соответсвующий ему объект Year

        self.__salary_dynamics (dict): Словарь, где ключ - год, а значение - средняя зарплата по всем вакансиям
                                       в этот год
        self.__num_vacancies_dynamics (dict): Словарь, где ключ - год, а значение - количество вакансий в этот год
        self.__selected_salary_dynamics (dict): Словарь, где ключ - год, а значение - средняя зарплата среди вакансий с
                                         выбранным названием в этот год
        self.__selected_num_vacancies_dynamics (dict): Словарь, где ключ - год, а значение - количество вакансий с
                                         выбранным названием в этот год
        self.__city_salary_dynamics (dict): Словарь, где ключ - название города, а значение - средняя зарплата
                                            в этом городе
        self.__city_num_vacancies_dynamics (dict): Словарь, где ключ - название города, а значение - количество
                                                   вакансий в этом городе

        self.__fulfillment (bool): Была ли посчитана статистика
    """

    def __init__(self, keywords: list, unwanted_words: list, data: list):
        """Инициализирует объект Statistic

        Args:
            keywords (list): Выбранное название вакансии для дополнительной статистики
            data (list): Список словарей с вакансиями
        """

        self.__keywords = keywords
        self.__unwanted_words = unwanted_words
        self.__vacancies_count = 0
        self.__cities = {}
        self.__years = {}

        self.__salary_dynamics = {}
        self.__num_vacancies_dynamics = {}
        self.__selected_salary_dynamics = {}
        self.__selected_num_vacancies_dynamics = {}
        self.__city_salary_dynamics = {}
        self.__city_num_vacancies_dynamics = {}
        self.__top_skills_by_year = {}

        self.__fulfillment = False
        self.enter_static_data(data)

    @property
    @check_statistics_preparedness
    def top_skills_by_year(self):
        return self.__top_skills_by_year

    @property
    @check_statistics_preparedness
    def salary_dynamics(self):
        """Возвращает значение приватного поля с динамикой зарплат"""

        return self.__salary_dynamics

    @property
    @check_statistics_preparedness
    def num_vacancies_dynamics(self):
        """Возвращает значение приватного поля с динамикой количества вакансий"""

        return self.__num_vacancies_dynamics

    @property
    @check_statistics_preparedness
    def selected_salary_dynamics(self):
        """Возвращает значение приватного поля с динамикой зарплат для вакансий с выбранным названием"""

        return self.__selected_salary_dynamics

    @property
    @check_statistics_preparedness
    def selected_num_vacancies_dynamics(self):
        """Возвращает значение приватного поля с динамикой количества вакансий с выбранным названием"""

        return self.__selected_num_vacancies_dynamics

    @property
    @check_statistics_preparedness
    def city_salary_dynamics(self):
        """Возвращает значение приватного поля со статистикой зарплат по городам"""

        return self.__city_salary_dynamics

    @property
    @check_statistics_preparedness
    def city_num_vacancies_dynamics(self):
        """Возвращает значение приватного поля со статистикой количества вакансий по городам"""

        return self.__city_num_vacancies_dynamics

    @property
    def years(self):
        """Возвращает значение приватного поля со словарём  (номер года: Year)"""

        return self.__years

    @property
    def cities(self):
        """Возвращает значение приватного поля со словарём  (название города: Year)"""

        return self.__cities

    @property
    def keywords(self):
        """Возвращает значение приватного поля с выбранным названием вакансии"""

        return self.__keywords

    @property
    def fulfillment(self):
        """Возвращает значение приватного поля со значением того, была ли посчитана статистика"""

        return self.__fulfillment

    @check_statistics_preparedness
    def get_vacancies_percentage(self, city_name):
        return self.__city_num_vacancies_dynamics[city_name] // self.__cities[city_name].vacancy_count

    def enter_static_data(self, data):
        """Заносит в Statistic все вакансии из списка

        Args:
            data (list): Список словарей с вакансиями
        """

        for row_dict in data:
            self.update(row_dict)

    def update(self, row_dict: dict):
        """Обновляет поля Statistic данными одной вакансии

        Args:
            row_dict (dict): Словарь вакансии
        """

        vacancy = Vacancy(row_dict)
        if vacancy.area_name not in self.__cities.keys():
            self.__cities[vacancy.area_name] = City(vacancy)
        else:
            self.__cities[vacancy.area_name].update(vacancy)
        if vacancy.year not in self.__years.keys():
            self.__years[vacancy.year] = Year(vacancy, self.__keywords, self.__unwanted_words)
        else:
            self.__years[vacancy.year].update(vacancy)
        self.__vacancies_count += 1

    def calculate_skill_statistics(self):
        for year in self.__years.values():
            if len(year.skills) > 0:
                sorted_skills = dict(sorted(year.skills.items(), key=lambda x: x[1], reverse=True)[:10])
                self.__top_skills_by_year[year.name] = sorted_skills

    def calculate_statistics(self):
        """Считает статистику, сортирует словари статистики по убыванию"""

        for year in self.__years.values():
            self.__salary_dynamics[year.name] = math.floor(year.average_salary)
            self.__num_vacancies_dynamics[year.name] = year.vacancy_count
            self.__selected_salary_dynamics[year.name] = math.floor(year.selected_vacancy_average_salary)
            self.__selected_num_vacancies_dynamics[year.name] = year.selected_vacancy_count
        self.__cities = dict(filter(lambda x: x[1].vacancy_count >= (self.__vacancies_count / 100),
                                    self.__cities.items()))
        self.__city_salary_dynamics = dict(sorted(self.__cities.items(),
                                                  key=lambda x: x[1].average_salary)[:10])
        self.__city_salary_dynamics = {key: math.floor(val.average_salary)
                                       for key, val in self.__city_salary_dynamics.items()}
        self.__city_num_vacancies_dynamics = dict(sorted(self.__cities.items(),
                                                         key=lambda x: x[1].vacancy_count)[:10])
        self.__city_num_vacancies_dynamics = {key: round(val.vacancy_count / self.__vacancies_count, 4)
                                              for key, val in self.__city_num_vacancies_dynamics.items()}
        self.calculate_skill_statistics()
        self.__fulfillment = True
