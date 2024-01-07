from abc import ABC, abstractmethod
import requests
import pprint


class ParsingError(Exception):
    def __str__(self):
        return "Ошибка подключения по API"


class Engine(ABC):
    """Абстрактный класс"""

    @abstractmethod
    def get_request(self):
        pass

    def get_vacancies(self):
        pass


class HeadHunter(Engine):
    """
    Класс API по hh.ru
    """

    def __init__(self):
        #self.keyword = keyword
        self.__header = {
            "User-Agent": "kostik80_80@mail.ru"}
        self.__params = {
            #"text": keyword,
            "employer_id": [
                "742313",
                "9106459",
                "5205718",
                "246290",
                "1743904",
                "3518049",
                "2501280",
                "1677761",
                "10258831",
                "10060651",
            ],
            "page": 0,
            "per_page": 20,
        }
        self.__vacancies = []  # список вакансий, который заполняется  по мерере получения данных по api

    @staticmethod
    def get_salary(salary):
        if salary is not None:
            if salary['from'] is not None and salary['to'] is not None:
                return round((salary['from'] + salary['to']) / 2)
            elif salary['from'] is not None:
                return salary['from']
            elif salary['to'] is not None:
                return salary['to']
        return None

    def get_request(self):
        """
        Получение значений через API
        """
        response = requests.get("https://api.hh.ru/vacancies", headers=self.__header, params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()["items"]

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary = self.get_salary(vacancy["salary"])
            formatted_vacancies.append({
                "vacancy_id": vacancy["id"],
                "vacancy_name": vacancy["name"],
                "vacancy_city": vacancy["area"]["name"],
                "salary": salary,
                "vacancy_url": vacancy["alternate_url"],
                "employer_id": vacancy["employer"]["id"],
                "employer_name": vacancy["employer"]["name"],
                "employer_url": vacancy["employer"]["url"],
            })

        return formatted_vacancies

    def get_vacancies(self, pages_count=1):
        while self.__params["page"] < pages_count:
            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print("Ошибка при получении данных")
                break
            print(f"Найдено ({len(values)}) вакансий")
            self.__vacancies.extend(values)
            self.__params["page"] += 1




# def main():
#     vacancies_json = []
#     #keyword = input("Введите профессию или должность: ")
#
#     hh = HeadHunter()
#
#     hh.get_vacancies(pages_count=5)
#     vacancies_json.extend(hh.get_formatted_vacancies())
#     pprint.pprint(vacancies_json)
#
#
# main()
#keyword = input("Введите профессию: ")
# hh = HeadHunter()
# pprint.pprint(hh.get_request())
