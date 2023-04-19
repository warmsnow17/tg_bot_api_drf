import requests, json
from loguru import logger


class Interface():
    cities_url = "http://web:8000/api/v1/cities/"
    suggestions_url = "http://web:8000/api/v1/suggestions/"
    reports_url = "http://web:8000/api/v1/reports/"
    ratings_url = "http://web:8000/api/v1/ratings/"

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
                        return (True, road['repair_date'])
                    else:
                        return (False,)
        return (False, None)

    def send_report(self, data, url):
        response = requests.post(url,
                                 data=data)
        logger.warning(response.json())
        if response.status_code == 201:
            return True

    def get_road_id_by_name(self, road_name: str):
        data = requests.get(self.cities_url).json()
        for city in data:
            for road in city['roads']:
                if road['name'] == road_name:
                    return road['id']
        return None


interface = Interface()
