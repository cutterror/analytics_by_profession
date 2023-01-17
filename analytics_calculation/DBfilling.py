import DBconnection


path = r'C:\Users\User\Desktop\program\python\project\analytics\db.sqlite3'


def fill_all_databases(with_skills_statistic, without_skills_statistic):
    fill_demand_database(without_skills_statistic)
    fill_geography_salary_database(without_skills_statistic)
    fill_geography_percent_database(without_skills_statistic)
    fill_skill_database(with_skills_statistic)


def fill_demand_database(statistic):
    fill_db_with_lists(statistic, 'java_developer_analytic_demand',
                       ['year', 'average_salary', 'vacancy_num', 'selected_average_salary', 'selected_vacancy_num'],
                       lambda x: [[str(y), str(x.salary_dynamics[y]), str(x.num_vacancies_dynamics[y]),
                                   str(x.selected_salary_dynamics[y]), str(x.selected_num_vacancies_dynamics[y])]
                                  for y in x.years])


def fill_geography_salary_database(statistic):
    fill_db_with_lists(statistic, 'java_developer_analytic_geographysalary', ['city', 'average_salary'],
                       lambda x: [['\'' + str(y).replace(' ', '_') + '\'', str(x.city_salary_dynamics[y])]
                                  for y in x.city_salary_dynamics.keys()])


def fill_geography_percent_database(statistic):
    fill_db_with_lists(statistic, 'java_developer_analytic_geographypercent', ['city', 'percent_vacancy_num'],
                       lambda x: [['\'' + str(y) + '\'', str(x.city_num_vacancies_dynamics[y])]
                                  for y in x.city_num_vacancies_dynamics.keys()])


def fill_skill_database(statistic):
    def formatter(items):
        skill_list = []
        for year in items.top_skills_by_year.keys():
            for skill in items.top_skills_by_year[year].keys():
                skill_list.append(['\'' + skill + '\'', str(year), str(items.top_skills_by_year[year][skill])])
        return skill_list
    fill_db_with_lists(statistic, 'java_developer_analytic_skills', ['skill', 'year', 'skill_count'], formatter)


def fill_db_with_lists(items: list, table_name: str, column_names: list, format_func):
    items = format_func(items)
    DBconnection.insert_into(table_name, column_names, items, path)
