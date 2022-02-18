import os

import requests
from dotenv import load_dotenv
from terminaltables import SingleTable

from mapping_result import display_table_of_result
from show_vacancies_hh import get_hh_vacancies_info
from show_vacancies_superjob import get_sj_vacancies_info


if __name__ == '__main__':
    load_dotenv()
    superjob_api = os.getenv('API_SUPERJOB')

    languages_of_programming = [
        'TypeScript',
        'Swift',
        'Scala',
        'Objective-C',
        'Shell',
        'Go',
        'C',
        'C#',
        'C++',
        'PHP',
        'Ruby',
        'Python',
        'Java',
        'JavaScript'
    ]

    recruit_company = [
        'HeadHunter Moscow',
        'SuperJob Moscow'
    ]

    for company in recruit_company:
        vacancies_for_language = {}

        for language in languages_of_programming:
            if company == 'HeadHunter Moscow':
                vacancy_info = get_hh_vacancies_info(language)
            elif company == 'SuperJob Moscow':
                vacancy_info = get_sj_vacancies_info(superjob_api, language)

            vacancies_for_language.update({language: vacancy_info})

        display_table_of_result(vacancies_for_language, company)