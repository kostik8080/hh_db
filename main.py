from src.class_hh import HeadHunter
from src.utils import create_database, save_vacancies_to_db
from src.DBManager import DBManager


def main():
    # keyword = 'Python'          # Ключевое слово поиска на hh.ru
    page = 0  # Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    per_page = 22  # Кол-во вакансий на 1 странице (max 22)
    database_name = 'hh_bd'  # Название БД

    vacancies_json = []
    hh = HeadHunter()
    hh.get_vacancies(pages_count=6)
    vacancies_json.extend(hh.get_formatted_vacancies())

    create_database(database_name)
    #
    save_vacancies_to_db(database_name, vacancies_json)

    dbmanager = DBManager(database_name)

    print('Приветствую, выберите действие.')

    while True:

        print("""
            1 - Список employer и количество vacancies.
            2 - Список vacancies с указанием названия employer, vacancies, salary и URL на вакансию.
            3 - Средняя ЗП
            4 - Список vacancies, у которых salary выше средней.
            5 - Найти вакансии по ключевому слову.
                """)
        user_answer = input('Ваш выбор: ')

        if user_answer == '1':
            emp_info = dbmanager.get_companies_and_vacancies_count()
            for i in emp_info:
                print(*i)

        elif user_answer == '2':
            all_vac = dbmanager.get_all_vacancies()
            for i in all_vac:
                print(*i)

        elif user_answer == '3':
            avg_sal = dbmanager.get_avg_salary()
            for item in avg_sal:
                print("Средняя ЗП:", *item)

        elif user_answer == '4':
            vac = dbmanager.get_vacancies_with_higher_salary()
            for item in vac:
                print(*item)

        elif user_answer == '5':
            keyword = input('Введите ключевое слово: ').lower()
            vac = dbmanager.get_vacancies_with_keyword(keyword)
            for item in vac:
                print(*item)
        else:
            print("Такого варианта нет")

        print("Продолжить?")
        answer = input("Y/N: ").upper()
        if answer == 'N':
            print()
            print("!!Пока!!")
            break


if __name__ == '__main__':
    main()
