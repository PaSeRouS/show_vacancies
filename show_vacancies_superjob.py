import os

import requests
from dotenv import load_dotenv

from mapping_result import display_table_of_result
from predict_rub_salary import predict_rub_salary

def get_request_sj(language, url, headers):
	
	vacancies_params = {
		'keyword': language,
		'town': 'Москва'
	}

	response = requests.get(url, headers=headers, params=vacancies_params)
	response.raise_for_status()

	return response


def download_pages(response, language, url, headers):
	page = 0
	vacancies = []

	while page < 5: # Так как можно только 500 результатов
		page_params = {
			'keyword' : language,
			'town' : 'Москва',
			'page': page,
			'count': 100
		}

		page_response = requests.get(url, headers=headers, params=page_params)
		page_response.raise_for_status()

		page_data = page_response.json()['objects']
		page += 1
	
		vacancies.append(page_data)

	return vacancies


def show_sj_vacancies_info(api_key):
	vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'

	headers = {
		'X-Api-App-Id': api_key
	}

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

		response_sj = get_request_sj(language, vacancies_url, headers)
		vacancies = download_pages(response_sj, language, vacancies_url, headers)

		for page in vacancies:
			for vacancy in page:
				if (vacancy['payment_from'] or vacancy['payment_to']) and vacancy['currency'] == 'rub':
					sum_salary += predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])
					vacancies_processed += 1

		vacancy_info['vacancies_found'] = response_sj.json()['total']
		vacancy_info['vacancies_processed'] = vacancies_processed
		vacancy_info['average_salary'] = int(sum_salary/vacancies_processed)
		vacancies_for_language.update({language: vacancy_info})
	
	display_table_of_result(vacancies_for_language, 'SuperJob Moscow')


if __name__ == '__main__':
	load_dotenv()

	superjob_api = os.getenv('API_SUPERJOB')

	show_sj_vacancies_info(superjob_api)
		