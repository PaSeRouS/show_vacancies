import requests

from mapping_result import display_table_of_result
from predict_rub_salary import predict_rub_salary


def get_request_hh(language, url):
	vacancies_params = {
		'text' : language,
		'area' : 1, # Москва
		'period' : 30
	}

	response = requests.get(url, params=vacancies_params)
	response.raise_for_status()

	return response


def download_pages(response, language, url):
	if response.json()['found'] > 100:
		page = 0
		pages_number = 1

		vacancies = []

		while page < pages_number:
			page_params = {
				'text' : language,
				'area' : 1, # Москва
				'period' : 30,
				'page': page
			}

			page_response = requests.get(url, params=page_params)
			page_response.raise_for_status()

			pages_number = page_response.json()['pages']
			page_data = page_response.json()['items']
			page += 1
	
			vacancies.append(page_data)

	return vacancies


def show_hh_vacancies_info():
	vacancies_url = 'https://api.hh.ru/vacancies'

	languages_of_programming = [
		'TypeScript',
		# 'Swift',
		# 'Scala',
		# 'Objective-C',
		# 'Shell',
		# 'Go',
		# 'C',
		# 'C#',
		# 'C++',
		# 'PHP',
		# 'Ruby',
		# 'Python',
		# 'Java',
		# 'JavaScript'
	]

	vacancies_for_language = {}

	for language in languages_of_programming:
		vacancy_info = {}

		vacancies_processed = 0
		sum_salary = 0

		response_hh = get_request_hh(language, vacancies_url)
		vacancies = download_pages(response_hh, language, vacancies_url)

		for page in vacancies:
			for vacancy in page:
				if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
					sum_salary += predict_rub_salary(vacancy['salary']['from'], vacancy['salary']['to'])
					vacancies_processed += 1

		vacancy_info['vacancies_found'] = response_hh.json()['found']
		vacancy_info['vacancies_processed'] = vacancies_processed
		vacancy_info['average_salary'] = int(sum_salary/vacancies_processed)

		vacancies_for_language.update({language: vacancy_info})


	display_table_of_result(vacancies_for_language, 'HeadHunter Moscow')


if __name__ == '__main__':
	show_hh_vacancies_info()
	