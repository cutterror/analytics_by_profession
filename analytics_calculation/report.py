from openpyxl import Workbook
from openpyxl.styles import Border, Side, Font
from statistic import Statistic
import matplotlib.pyplot as plt
import numpy as np
import os


def select_directory(patch: str, directory_name: str):
    if os.getcwd()[len(os.getcwd()) - len(directory_name):] != directory_name:
        os.chdir(patch)


class Report:
    """Класс для генерации файлов с отчётами по статистическим данным

    Attributes:
        self.__statistic (Statistic): статистика для генерации отчётов
        self.__book (Workbook): excel книга, содержащая старницы с отчётами
        self.__year_list (Worksheet): страница со статистикой по годам
        self.__city_list (Worksheet): страница со статистикой по городам
        fig, axs (Figure, ndarray): пространство для формирования графиков
    """

    """Статические поля с конфигурацией файлов"""
    title_font = Font(name='Calibri', size=11, bold=True)
    border = Border(left=Side(border_style="thin", color='FF000000'),
                    right=Side(border_style="thin", color='FF000000'),
                    top=Side(border_style="thin", color='FF000000'),
                    bottom=Side(border_style="thin", color='FF000000'))
    fig_height, fig_width = 13, 13

    def __init__(self, statistic: Statistic):
        """Инициализирует объект Report

        Args:
            statistic (Statistic): Статистика для формирования отчётов
        """

        self.__statistic = statistic
        self.__book = Workbook()
        self.__year_list = self.__book.active
        self.__year_list.title = "Статистика по годам"
        self.__city_list = self.__book.create_sheet("Статистика по городам")
        self.fig, self.axs = plt.subplots()
        self.fig.set_figheight(self.fig_height)
        self.fig.set_figwidth(self.fig_width)
        plt.rc('axes', titlesize=20)

    def generate_images(self):
        """Генерирует png-изображение с граффиками по статистике зарплат, количеству вакансий"""
        select_directory('../analytics/java_developer_analytic/static/images', 'images')
        self.create_one_labels_graph(self.__statistic.salary_dynamics.values(), 'средняя з/п',
                                     self.__statistic.salary_dynamics.keys(), 'Средний уровень зарплат по годам',
                                     'salary_dynamics.png')
        self.create_one_labels_graph(self.__statistic.num_vacancies_dynamics.values(), 'количество вакансий',
                                     self.__statistic.num_vacancies_dynamics.keys(), 'Количество вакансий по годам',
                                     'num_vacancies_dynamics.png')
        self.create_one_labels_graph(self.__statistic.selected_salary_dynamics.values(), 'средняя з/п',
                                     self.__statistic.selected_salary_dynamics.keys(),
                                     'Средний уровень зарплат по годам для ' + ', '.join(self.__statistic.keywords),
                                     'selected_salary_dynamics.png')
        self.create_one_labels_graph(self.__statistic.selected_num_vacancies_dynamics.values(), 'количество вакансий',
                                     self.__statistic.num_vacancies_dynamics.keys(),
                                     'Количество вакансий - \"' + ', '.join(self.__statistic.keywords) + '\" по годам',
                                     'selected_num_vacancies_dynamics.png')
        self.create_one_labels_graph(self.__statistic.city_salary_dynamics.values(), 'средняя з/п',
                                     self.__statistic.city_salary_dynamics.keys(),
                                     'Уровень средних зарплат по городам',
                                     'city_salary_dynamics.png')
        self.create_one_labels_graph(self.__statistic.city_num_vacancies_dynamics.values(), 'количество вакансий',
                                     self.__statistic.city_num_vacancies_dynamics.keys(),
                                     'Количество вакансий по городам',
                                     'city_num_vacancies_dynamics.png')
        select_directory('../../../../analytics_calculation', 'analytics_calculation')

    def generate_skills_images(self):
        """Генерирует png-изображение с граффиками по статистике требуемых навыков за определенный год"""
        select_directory('../analytics/java_developer_analytic/static/images', 'images')
        for year in self.__statistic.top_skills_by_year.keys():
            self.create_one_labels_graph(self.__statistic.top_skills_by_year[year].values(), 'количество упоминаний',
                                         self.__statistic.top_skills_by_year[year].keys(),
                                         f'Навыки по количеству упоминаний за {year} год',
                                         f'{year}.png')
        select_directory('../../../../analytics_calculation', 'analytics_calculation')

    def create_one_labels_graph(self, first_labels, first_labels_name: str, ticks, title: str, file_name: str):
        """Добавляет в изображение граффик с одним набороб столбцов
        """

        self.reset_chart()
        slots = np.arange(len(ticks))
        width = 0.35
        self.axs.bar(slots, first_labels, width, label=first_labels_name)
        self.axs.set_title(title)
        self.axs.set_xticks(slots, ticks, rotation=90)
        self.axs.yaxis.grid(visible=True, which='major', color='grey', alpha=.25)
        self.axs.legend()
        plt.savefig(file_name, dpi=250)

    def reset_chart(self):
        """Сбрасывает поле для рисования граффиков, чтобы они не наслаивались
        """

        self.fig.clf()
        self.fig, self.axs = plt.subplots()
        self.fig.set_figheight(self.fig_height)
        self.fig.set_figwidth(self.fig_width)
        plt.rc('axes', titlesize=20)

    def prepare_demand_tables(self):
        select_directory('../analytics/java_developer_analytic/templates', 'templates')
        salary_dynamics = create_html_tables(
            len(self.__statistic.salary_dynamics.keys()), ['year', 'salary'], 'Динамика уровня зарплат по годам',
            ['Год', 'Средняя зарплата'], 'salary_dynamics')
        paste_in_html('demand.html', 'demand.html', salary_dynamics, '<!--salary-dynamics_table-->')
        num_vacancies_dynamics = create_html_tables(
            len(self.__statistic.num_vacancies_dynamics.keys()), ['year', 'num'],
            'Динамика количества вакансий по годам', ['Год', 'Количество вакансий'], 'num_vacancies_dynamics')
        paste_in_html('demand.html', 'demand.html', num_vacancies_dynamics, '<!--num_vacancies_dynamics_table-->')
        selected_salary_dynamics = create_html_tables(
            len(self.__statistic.selected_salary_dynamics.keys()), ['year', 'salary_sel'],
            'Динамика уровня зарплат по годам для Java-программиста', ['Год', 'Средняя зарплата - Java-программист'],
            'selected_salary_dynamics')
        paste_in_html('demand.html', 'demand.html', selected_salary_dynamics,
                           '<!--selected_salary_dynamics_table-->')
        selected_num_vacancies_dynamics = create_html_tables(
            len(self.__statistic.selected_num_vacancies_dynamics.keys()), ['year', 'num_sel'],
            'Динамика количества вакансий по годам для Java-программиста',
            ['Год', 'Количество вакансий - Java-программист'], 'selected_num_vacancies_dynamics')
        paste_in_html('demand.html', 'demand.html', selected_num_vacancies_dynamics,
                           '<!--selected_num_vacancies_dynamics_table-->')
        select_directory('../../../analytics_calculation', 'analytics_calculation')

    def prepare_geography_tables(self):
        select_directory('../analytics/java_developer_analytic/templates', 'templates')
        cities_salary = create_html_tables(
            len(self.__statistic.city_salary_dynamics.keys()), ['city', 'salary'],
            'Уровень зарплат по городам - топ 10, начиная с конца',
            ['Город', 'Средняя зарплата'], 'city_salary_dynamics')
        paste_in_html('geography.html', 'geography.html', cities_salary, '<!--cities_salary_table-->')
        cities_vacancy_num = create_html_tables(
            len(self.__statistic.city_num_vacancies_dynamics.keys()), ['city_per', 'percent'],
            'Доля вакансий по городам - топ 10, начиная с конца',
            ['Город', 'Доля вакансий'], 'city_num_vacancies_dynamics')
        paste_in_html('geography.html', 'geography.html', cities_vacancy_num, '<!--cities_vacancy_num_table-->')
        select_directory('../../../analytics_calculation', 'analytics_calculation')

    def prepare_skills_tables(self):
        select_directory('../analytics/java_developer_analytic/templates', 'templates')
        skill_tables = ''
        for i, year in enumerate(self.__statistic.top_skills_by_year.keys()):
            skill_tables += create_html_tables(
                len(self.__statistic.city_salary_dynamics.keys()), ['skill' + str(i) + '_', 'count' + str(i) + '_'],
                '{{ year' + str(i) + ' }}', ['Навык', 'Сколько раз встречается в вакансиях'], str(year))
        paste_in_html('skills.html', 'skills.html', skill_tables, '<!--skill_tables-->')
        select_directory('../../../analytics_calculation', 'analytics_calculation')


def paste_in_html(file_name: str, new_file_name: str, string: str, string_name: str):
    file = open(file_name, "r", encoding='utf-8-sig')
    html = file.read()
    file.close()
    new_html = html.replace(string_name, string)
    new_file = open(new_file_name, "w+", encoding='utf-8-sig')
    new_file.write(new_html)
    new_file.close()


def create_html_tables(length: int, inserts: list, table_name: str, column_names: list, img_name: str):
    table_template = f'<div class="section"><table border="1"><caption>{table_name}</caption><tr>'
    for column_name in column_names:
        table_template += f'<th>{column_name}</th>'
    table_template += '</tr>'
    for i in range(length):
        table_template += '<tr>'
        for insert in inserts:
            table_template += '<td>{{ ' + insert + str(i) + ' }}</td>'
        table_template += '</tr>'
    table_template += '''</table><img src="{% static 'images/''' + img_name + '''.png' %}"></div>'''
    return table_template
