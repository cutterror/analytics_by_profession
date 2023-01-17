from dataset import DataSet
from report import Report
from statistic import Statistic
import DBfilling


def calculate_statistics(file_name: str, keywords: list,
                         unwanted_words: list):
    """Считает статистику и производит необходимые манипуляции с ней
    """

    data = DataSet(file_name).data
    statistic = Statistic(keywords, unwanted_words, data)
    statistic.calculate_statistics()

    # DBfilling.fill_all_databases(statistic)

    report = Report(statistic)
    report.generate_all_images()
    report.prepare_all_tables()


calculate_statistics('vacancies_with_skills.csv', ['java', 'ява', 'джава'], ['фронт', 'front', 'javascript'])
