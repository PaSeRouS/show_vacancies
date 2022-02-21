import os
from itertools import count

import requests
from dotenv import load_dotenv

from mapping_result import display_table_of_result
from predict_rub_salary import predict_rub_salary


def get_pages_data(language, url, headers):
    vacancies = []

    for page in count(0):
        page_params = {
            'keyword' : language,
            'town' : 'Москва',
            'page': page,
            'count': 100
        }

        page_response = requests.get(url, headers=headers, params=page_params)
        page_response.raise_for_status()

        page_data = page_response.json()
        vacancies.append(page_data['objects'])

        if page >= 4: # Так как можно только 500 результатов
            break

    total_vacancies = page_data['total']

    return vacancies, total_vacancies


def get_sj_vacancies_info(api_key, language):
    vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'

    headers = {
        'X-Api-App-Id': api_key
    }

    vacancy_info = {}

    vacancies_processed = 0
    sum_salary = 0

    vacancies_params = {
        'keyword': language,
        'town': 'Москва'
    }

    vacancies, total_vacancies = get_pages_data(language, vacancies_url, headers)

    for page in vacancies:
        for vacancy in page:
            if (vacancy['payment_from'] or vacancy['payment_to']) and vacancy['currency'] == 'rub':
                sum_salary += predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])
                vacancies_processed += 1

    vacancy_info['vacancies_found'] = total_vacancies
    vacancy_info['vacancies_processed'] = vacancies_processed
    vacancy_info['average_salary'] = int(sum_salary/vacancies_processed)
	
    return vacancy_info


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

    vacancies_for_language = {}

    for language in languages_of_programming:
        vacancy_info = get_sj_vacancies_info(superjob_api, language)
        vacancies_for_language.update({language: vacancy_info})

    display_table_of_result(vacancies_for_language, 'SuperJob Moscow')
		