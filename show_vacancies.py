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

    vacancies_hh_for_language = {}
    vacancies_sj_for_language = {}

    for language in languages_of_programming:
        vacancy_info = get_hh_vacancies_info(language)
        vacancies_hh_for_language.update({language: vacancy_info})

        vacancy_info = get_sj_vacancies_info(superjob_api, language)
        vacancies_sj_for_language.update({language: vacancy_info})

    display_table_of_result(vacancies_hh_for_language, 'HeadHunter Moscow')
    display_table_of_result(vacancies_sj_for_language, 'SuperJob Moscow')