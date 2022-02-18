from itertools import count

import requests

from mapping_result import display_table_of_result
from predict_rub_salary import predict_rub_salary


def get_pages_data(language, url):
	page = 0

	vacancies = []

	for page in count(0):
		page_params = {
			'text' : language,
			'area' : 1, # Москва
			'period' : 30,
			'page': page
		}

		page_response = requests.get(url, params=page_params)
		page_response.raise_for_status()

		page_data = page_response.json()
		if page >= (page_data['pages'] - 1):
			break
	
		vacancies.append(page_data['items'])

	return vacancies


def get_hh_vacancies_info(language):
	vacancies_url = 'https://api.hh.ru/vacancies'

	vacancy_info = {}

	vacancies_processed = 0
	sum_salary = 0

	vacancies_params = {
		'text' : language,
		'area' : 1, # Москва
		'period' : 30
	}

	response = requests.get(vacancies_url, params=vacancies_params)
	response.raise_for_status()

	vacancies = get_pages_data(language, vacancies_url)

	for page in vacancies:
		for vacancy in page:
			if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
				sum_salary += predict_rub_salary(vacancy['salary']['from'], vacancy['salary']['to'])
				vacancies_processed += 1

	vacancy_info['vacancies_found'] = response.json()['found']
	vacancy_info['vacancies_processed'] = vacancies_processed
	vacancy_info['average_salary'] = int(sum_salary/vacancies_processed)

	return vacancy_info


if __name__ == '__main__':
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
		vacancy_info = get_hh_vacancies_info(language)
		vacancies_for_language.update({language: vacancy_info})

	display_table_of_result(vacancies_for_language, 'HeadHunter Moscow')
	