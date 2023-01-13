from openpyxl import Workbook
from openpyxl.styles import Border, Side, Font
from statistic import Statistic
import matplotlib.pyplot as plt
import numpy as np
from string import Template
import os


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
        """Генерирует png-изображение с граффиками по статистике"""
        os.chdir('../analytics/java_developer_analytic/static/images')
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
                                     'Уровень средних зарплат по городам (в порядке убывания)',
                                     'city_salary_dynamics.png')
        self.create_one_labels_graph(self.__statistic.city_num_vacancies_dynamics.values(), 'количество вакансий',
                                     self.__statistic.city_num_vacancies_dynamics.keys(),
                                     'Количество вакансий по городам (в порядке убывания)',
                                     'city_num_vacancies_dynamics.png')
        self.generate_skills_images()

    def generate_skills_images(self):
        for year in self.__statistic.top_skills_by_year.keys():
            self.create_one_labels_graph(self.__statistic.top_skills_by_year[year].values(), 'количество упоминаний',
                                         self.__statistic.top_skills_by_year[year].keys(),
                                         f'Навыки по количеству упоминаний за {year} год',
                                         f'{year}.png')

    def create_one_labels_graph(self, first_labels, first_labels_name: str, ticks, title: str, file_name: str):
        """Добавляет в изображение граффик с одним набороб столбцов
        """

        slots = np.arange(len(ticks))
        width = 0.35
        self.axs.bar(slots, first_labels, width, label=first_labels_name)
        self.axs.set_title(title)
        self.axs.set_xticks(slots, ticks, rotation=90)
        self.axs.yaxis.grid(visible=True, which='major', color='grey', alpha=.25)
        self.axs.legend()
        plt.savefig(file_name, dpi=250)
        self.reset_chart()

    def reset_chart(self):
        self.fig.clf()
        self.fig, self.axs = plt.subplots()
        self.fig.set_figheight(self.fig_height)
        self.fig.set_figwidth(self.fig_width)
        plt.rc('axes', titlesize=20)

    def render_html_tables(self):
        os.chdir('../../templates')
        self.render_html_table('geography.html')

    def render_html_table(self, file_name: str):
        salary_dynamics = self.create_html_statistics_trs(lambda x: x, self.__statistic.salary_dynamics)
        num_vacancies_dynamics = self.create_html_statistics_trs(lambda x: x, self.__statistic.num_vacancies_dynamics)
        selected_salary_dynamics = self.create_html_statistics_trs(lambda x: x,
                                                                   self.__statistic.selected_salary_dynamics)
        selected_num_vacancies_dynamics = self.create_html_statistics_trs(lambda x: x,
                                                                          self.__statistic.selected_num_vacancies_dynamics)
        cities_salary_statistics_trs = self.create_html_statistics_trs(lambda x: x,
                                                                       self.__statistic.city_salary_dynamics)
        cities_vacancy_num_statistics_trs = self.create_html_statistics_trs(
            lambda x: str(round(x * 100, 2)) + '%', self.__statistic.city_salary_dynamics)
        skills_tables = self.create_html_statistics_tables(self.__statistic.top_skills_by_year)

        self.paste_in_html('geography.html', 'geography.html', cities_salary_statistics_trs,
                           '!cities_salary_statistics_trs!')
        self.paste_in_html('geography.html', 'geography.html', cities_vacancy_num_statistics_trs,
                           '!cities_vacancy_num_statistics_trs!')
        self.paste_in_html('demand.html', 'demand.html', salary_dynamics,
                           '!salary_dynamics!')
        self.paste_in_html('demand.html', 'demand.html', num_vacancies_dynamics,
                           '!num_vacancies_dynamics!')
        self.paste_in_html('demand.html', 'demand.html', selected_salary_dynamics,
                           '!selected_salary_dynamics!')
        self.paste_in_html('demand.html', 'demand.html', selected_num_vacancies_dynamics,
                           '!selected_num_vacancies_dynamics!')
        self.paste_in_html('skills.html', 'skills.html', skills_tables,
                           '!skills_tables!')

    def paste_in_html(self, file_name: str, new_file_name: str, string: str, string_name: str):
        file = open(file_name, "r", encoding='utf-8-sig')
        html = file.read()
        file.close()
        new_html = html.replace(string_name, string)
        new_file = open(new_file_name, "w+", encoding='utf-8-sig')
        new_file.write(new_html)
        new_file.close()

    def create_html_years_statistics_trs(self):
        """Заполняет таблицу в pdf файле статистистикой по годам"""

        tr_template = ''
        for year in self.__statistic.years:
            average_salary = self.__statistic.salary_dynamics[year]
            selected_average_salary = self.__statistic.selected_salary_dynamics[year]
            vacancies_number = self.__statistic.num_vacancies_dynamics[year]
            selected_vacancies_number = self.__statistic.selected_num_vacancies_dynamics[year]
            tr_template += f'<tr><td class="year">{year}</td><td>{average_salary}</td><td>{selected_average_salary}' + \
                           f'</td><td>{vacancies_number}</td><td>{selected_vacancies_number}</td></tr>'
        return tr_template

    def create_html_statistics_trs(self, format_function, statistics):
        """Заполняет таблицу в pdf файле статистистикой по городам, применяя форматирование данных
        """

        tr_template = ''
        for element in statistics.keys():
            statistic_value = format_function(statistics[element])
            tr_template += f'<tr><td>{element}</td><td>{statistic_value}</td></tr>'
        return tr_template

    def create_html_statistics_tables(self, statistics):
        table_template = ''
        for table_element in statistics.keys():
            table_template += f'<div class="section"><table border="1"><caption>{table_element}</caption><tr><th>Навык' \
                              f'</th><th>Сколько раз встречается в вакансиях</th></tr>'
            image_src = "{% static 'images/" + str(table_element) + ".png' %}"
            for tr_element in statistics[table_element].keys():
                statistic_value = statistics[table_element][tr_element]
                table_template += f'<tr><td>{tr_element}</td><td>{statistic_value}</td></tr>'
            table_template += f"</table><img src=\"{image_src}\"></div>"
        return table_template
