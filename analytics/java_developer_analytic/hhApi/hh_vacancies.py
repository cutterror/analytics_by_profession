from urllib.parse import urlparse, urlencode
import requests


class HHJavaVacancies:
    keywords = ['java', 'ява', 'джава']
    start_url = urlparse("https://api.hh.ru/vacancies/")

    def __init__(self, per_page=10, search_field="name", order_by="publication_time"):
        query = {
            "text": " OR ".join(self.keywords),
            "search_field": search_field,
            "per_page": str(per_page),
            "order_by": order_by
        }
        url = self.start_url._replace(query=urlencode(query))
        responce = requests.get(url.geturl())
        items = responce.json()["items"]

        self.vacancies = items
