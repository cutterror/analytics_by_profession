from dataset import DataSet
from report import Report
from statistic import Statistic


def print_statistics_report(vacancy_data: list):
    """Считает статистику и генерирует файлы с ней

    Args:
        vacancy_data (list): Список словарей с вакансиями для статистики
    """

    keywords = ['java', 'ява', 'джава']
    unwanted_words = ['фронт', 'front', 'javascript']
    statistic = Statistic(keywords, unwanted_words, vacancy_data)
    report = Report(statistic)
    report.generate_images()
    report.render_html_tables()


file_name = 'vacancies_dif_currencies.csv'
data = DataSet(file_name).data
print_statistics_report(data)
