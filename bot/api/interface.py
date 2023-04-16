import requests, json
from loguru import logger


class Interface():
    cities_url = "http://127.0.0.1:8000/api/v1/cities/"
    suggestions_url = "http://127.0.0.1:8000/api/v1/suggestions/"
    reports_url = "http://127.0.0.1:8000/api/v1/reports/"
    ratings_url = "http://127.0.0.1:8000/api/v1/ratings/"

    def get_cities_names(self):
        data = requests.get(self.cities_url).json()
        names = [(city['name'], city['pk']) for city in data]
        return names

    def get_roads(self, id):
        data = requests.get(self.cities_url).json()
        streets = []
        for city in data:
            if city['pk'] == id:
                for road in city['roads']:
                    streets.append((road['name'], road['id']))

                logger.warning(streets)
        return streets

    def check_status(self, road_id):
        data = requests.get(self.cities_url).json()
        for city in data:
            for road in city['roads']:
                if road['id'] == road_id:
                    if road['status'] == 'WT':
                        return True

    def send_report(self, data):
        response = requests.post('http://127.0.0.1:8000/api/v1/reports/',
                                 data=data)
        logger.warning(response.json())
        if response.status_code == 201:
            return True


interface = Interface()
