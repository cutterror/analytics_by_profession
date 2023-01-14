from dataset import DataSet
from report import Report
from statistic import Statistic
import DBconnection


def fill_demand_database(statistic):
    demand_list = [[year, statistic.salary_dynamics[year], statistic.num_vacancies_dynamics[year],
                    statistic.selected_salary_dynamics[year], statistic.selected_num_vacancies_dynamics[year]]
                   for year in statistic.years]
    demand_list = [[str(x) for x in items_list] for items_list in demand_list]
    demand_column_names = ['year', 'average_salary', 'vacancy_num', 'selected_average_salary', 'selected_vacancy_num']
    DBconnection.insert_into('java_developer_analytic_demand', demand_column_names, demand_list)


def fill_geography_salary_database(statistic):
    geography_salary_list = [[city, statistic.city_salary_dynamics[city]]
                             for city in statistic.city_salary_dynamics.keys()]
    geography_salary_list = [[str(x).replace(' ', '_') if ' ' in str(x) else str(x) for x in items_list]
                             for items_list in geography_salary_list]
    for i in range(len(geography_salary_list)):
        geography_salary_list[i][0] = '\'' + geography_salary_list[i][0] + '\''
    geography_column_names = ['city', 'average_salary']
    DBconnection.insert_into('java_developer_analytic_geographysalary', geography_column_names, geography_salary_list)


def fill_geography_percent_database(statistic):
    geography_percent_list = [[city, statistic.city_num_vacancies_dynamics[city]]
                              for city in statistic.city_num_vacancies_dynamics.keys()]
    geography_percent_list = [[str(x) for x in items_list] for items_list in geography_percent_list]
    for i in range(len(geography_percent_list)):
        geography_percent_list[i][0] = '\'' + geography_percent_list[i][0] + '\''
    geography_percent_names = ['city', 'percent_vacancy_num']
    DBconnection.insert_into('java_developer_analytic_geographypercent', geography_percent_names,
                             geography_percent_list)


def fill_skill_database(statistic):
    skill_list = []
    for year in statistic.top_skills_by_year.keys():
        for skill in statistic.top_skills_by_year[year].keys():
            skill_list.append(['\'' + skill + '\'', str(year), str(statistic.top_skills_by_year[year][skill])])
    geography_percent_names = ['skill', 'year', 'skill_count']
    DBconnection.insert_into('java_developer_analytic_skills', geography_percent_names,
                             skill_list)


def print_statistics_report(vacancy_data: list):
    """Считает статистику и генерирует файлы с ней

    Args:
        vacancy_data (list): Список словарей с вакансиями для статистики
    """

    keywords = ['java', 'ява', 'джава']
    unwanted_words = ['фронт', 'front', 'javascript']
    statistic = Statistic(keywords, unwanted_words, vacancy_data)

    # report = Report(statistic)
    # report.generate_images()
    # report.render_html_tables()


file_name = 'vacancies_with_skills.csv'
data = DataSet(file_name).data
print_statistics_report(data)
