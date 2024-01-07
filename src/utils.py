import psycopg2


def create_database(database_name: str) -> None:
    """Создание базы данных и таблиц для сохранения данных"""
    con = psycopg2.connect(database='postgres', host='localhost', user='postgres', password='12345')
    con.autocommit = True
    cur = con.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    con.close()

    conn = psycopg2.connect(database=database_name, host='localhost', user='postgres', password='12345')

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS employeers (
            employer_id int PRIMARY KEY,
            employer_name varchar(100) NOT NULL,
            employer_url varchar(255)
            );
            
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id int PRIMARY KEY,
            vacancy_name varchar(200) NOT NULL,
            vacancy_city varchar(100),
            salary int,
            vacancy_url varchar(255), 
            employer_id int REFERENCES employeers(employer_id)          
            );
        """)

    conn.commit()
    conn.close()


def save_vacancies_to_db(database_name: str, list_vacancies: list) -> None:
    """Записываем инфо по вакансиям в БД"""

    conn = psycopg2.connect(database=database_name, host='localhost',  user='postgres', password='12345')
    with conn:
        with conn.cursor() as cur:
            for vacancy in list_vacancies:
                cur.execute('INSERT INTO employeers (employer_id, employer_name, employer_url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (
                    vacancy['employer_id'],
                    vacancy['employer_name'],
                    vacancy['employer_url']
                ))
                cur.execute('INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_city, salary, vacancy_url, employer_id) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING', (
                    vacancy['vacancy_id'],
                    vacancy['vacancy_name'],
                    vacancy['vacancy_city'],
                    vacancy['salary'],
                    vacancy['vacancy_url'],
                    vacancy['employer_id']
                ))

    conn.commit()
    conn.close()

