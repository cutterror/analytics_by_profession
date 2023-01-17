from dataset import DataSet
from report import Report
from statistic import Statistic
import DBfilling


def calculate_statistics(without_skills_file_name: str, with_skills_file_name: str, keywords: list,
                         unwanted_words: list):
    """Считает статистику и генерирует файлы с ней
    """

    with_skills_data = DataSet(with_skills_file_name).data
    without_skills_data = DataSet(without_skills_file_name).data
    with_skills_statistic = Statistic(keywords, unwanted_words, with_skills_data)
    without_skills_statistic = Statistic(keywords, unwanted_words, without_skills_data)

    # DBfilling.fill_all_databases(with_skills_statistic, without_skills_statistic)

    with_skills_report = Report(with_skills_statistic)
    without_skills_report = Report(without_skills_statistic)

    without_skills_report.generate_images()
    with_skills_report.generate_skills_images()

    # report.generate_images()
    # report.render_html_tables()


calculate_statistics('vacancies_dif_currencies.csv', 'vacancies_with_skills.csv', ['java', 'ява', 'джава'],
                     ['фронт', 'front', 'javascript'])
