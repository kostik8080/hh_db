from typing import List, Tuple, Any

import psycopg2


class DBManager:
    def __init__(self, database_name):
        self.database_name = database_name

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """

        con = psycopg2.connect(database=self.database_name, host='localhost', user='postgres', password='12345')
        with con:
            with con.cursor() as cur:
                cur.execute(
                    """
                    SELECT employer_name, COUNT(*) as vacancies_quantity 
                    FROM employeers
                    JOIN vacancies USING(employer_id)
                    GROUP BY employer_name
                    ORDER BY vacancies_quantity DESC 
                    """
                )
                result = cur.fetchall()
        con.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        con = psycopg2.connect(database=self.database_name, host='localhost', user='postgres', password='12345')
        with con:
            with con.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.employer_name, v.vacancy_name, salary, v.vacancy_url 
                    FROM employeers e
                    JOIN vacancies v USING(employer_id)
                    ORDER BY salary DESC 
                    """
                )
                result = cur.fetchall()
        con.close()
        return result

    def get_avg_salary(self) -> list[tuple[Any, ...]]:
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(database=self.database_name, host='localhost', user='postgres', password='12345')

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT   round(AVG(salary)) AS average_salary  
                    FROM vacancies
                                       
                    """
                )
                results = []
                for result in cur.fetchall():  # Fetch all rows at once
                    results.append(result)

        conn.close()
        return results

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        conn = psycopg2.connect(database=self.database_name, host='localhost', user='postgres', password='12345')

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name, salary, vacancy_url 
                    FROM vacancies
                    WHERE salary > (SELECT AVG(salary) FROM vacancies)
                    
                    ORDER BY salary DESC
                    """
                )
                results = []
                for result in cur.fetchall():  # Fetch all rows at once
                    results.append(result)

        conn.close()
        return results

    def get_vacancies_with_keyword(self, keyword):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :param keyword:
        :return:
        """

        conn = psycopg2.connect(database=self.database_name, host='localhost', user='postgres', password='12345')

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT vacancy_name, salary, vacancy_url
                    FROM vacancies
                    WHERE lower(vacancy_name) LIKE '%{keyword}%'
                    """
                )
                results = []
                for result in cur.fetchall():  # Fetch all rows at once
                    results.append(result)

        conn.close()
        return results
