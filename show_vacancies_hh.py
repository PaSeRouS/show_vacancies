import requests

from mapping_result import display_table_of_result


def show_hh_vacancies_info():
	vacancies_url = 'https://api.hh.ru/vacancies'

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

		vacancies_params = {
			'text' : language,
			'area' : 1, # Москва
			'period' : 30
		}

		response = requests.get(vacancies_url, params=vacancies_params)
		response.raise_for_status()

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

				page_response = requests.get(vacancies_url, params=page_params)
				page_response.raise_for_status()

				pages_number = page_response.json()['pages']
				page += 1
	
				vacancies.append(page_response.json()['items'])

			vacancy_info['vacancies_found'] = response.json()['found']

			for page in vacancies:
				for vacancy in page:
					if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
						sum_salary += predict_rub_salary_for_hh(vacancy)
						vacancies_processed += 1

			vacancy_info['vacancies_processed'] = vacancies_processed
			vacancy_info['average_salary'] = int(sum_salary/vacancies_processed)

			vacancies_for_language.update({language: vacancy_info})

	display_table_of_result(vacancies_for_language, 'HeadHunter Moscow')


def predict_rub_salary_for_hh(vacancy):
	if vacancy['salary']['from'] and vacancy['salary']['to']:
		return (vacancy['salary']['from']+vacancy['salary']['to'])/2
	elif not vacancy['salary']['from'] and vacancy['salary']['to']:
		return vacancy['salary']['to']*0.8
	elif vacancy['salary']['from'] and not vacancy['salary']['to']:
		return vacancy['salary']['from']*1.2


if __name__ == '__main__':
	show_hh_vacancies_info()