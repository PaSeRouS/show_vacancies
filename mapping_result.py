from terminaltables import SingleTable


def mapping_result(results, title):
	table_data = [
		['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
	]

	for language in results:
		language_result = []
		language_result.append(language)
		language_result.append(results[language]['vacancies_found'])
		language_result.append(results[language]['vacancies_processed'])
		language_result.append(results[language]['average_salary'])

		table_data.append(language_result)

	table_instance = SingleTable(table_data, title)
	print(table_instance.table)
	print()