import csv


class DataSet:
    required_fields = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']

    def __init__(self, file_name: str):
        self.__file = open(file_name, 'r', encoding='utf-8-sig')
        self.__data = csv.reader(self.__file, delimiter=',')
        self.__titles = next(self.data)
        self.glue_row_dictionaries()

    @property
    def data(self):
        return self.__data

    @property
    def titles(self):
        return self.__titles

    def glue_row_dictionaries(self):
        def is_ok_row(row):
            for field in self.required_fields:
                if field not in row.keys() or row[field] == "":
                    return False
            return True

        self.__data = list(dict(zip(self.__titles, row)) for row in self.__data)
        self.__data = filter(is_ok_row, self.__data)
