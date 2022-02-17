import os

import requests
from dotenv import load_dotenv

from mapping_result import display_table_of_result


def show_sj_vacancies_info(api_key):
	vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'

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
		vacancy_info = {}

		vacancies_processed = 0
		sum_salary = 0

		headers = {
			'X-Api-App-Id': api_key
		}

		vacancies_params = {
			'keyword': language,
			'town': 'Москва'
		}

		response = requests.get(vacancies_url, headers=headers, params=vacancies_params)
		response.raise_for_status()

		page = 0

		vacancies = []

		while page < 5: # Так как можно только 500 результатов
			page_params = {
				'keyword' : language,
				'town' : 'Москва',
				'page': page,
				'count': 100
			}

			page_response = requests.get(vacancies_url, headers=headers, params=page_params)
			page_response.raise_for_status()

			page += 1
	
			vacancies.append(page_response.json()['objects'])

		vacancy_info['vacancies_found'] = response.json()['total']

		for page in vacancies:
			for vacancy in page:
				if (vacancy['payment_from'] or vacancy['payment_to']) and vacancy['currency'] == 'rub':
					sum_salary += predict_rub_salary_for_superjob(vacancy)
					vacancies_processed += 1

		vacancy_info['vacancies_processed'] = vacancies_processed
		vacancy_info['average_salary'] = int(sum_salary/vacancies_processed)

		vacancies_for_language.update({language: vacancy_info})

	display_table_of_result(vacancies_for_language, 'SuperJob Moscow')


def predict_rub_salary_for_superjob(vacancy):
	if vacancy['payment_from'] and vacancy['payment_to']:
		return (vacancy['payment_from']+vacancy['payment_to'])/2
	elif not vacancy['payment_from'] and vacancy['payment_to']:
		return vacancy['payment_to']*0.8
	elif vacancy['payment_from'] and not vacancy['payment_to']:
		return vacancy['payment_from']*1.2


if __name__ == '__main__':
	load_dotenv()

	superjob_api = os.getenv('API_SUPERJOB')

	show_sj_vacancies_info(superjob_api)