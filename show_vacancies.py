import os

import requests
from dotenv import load_dotenv
from terminaltables import SingleTable

from mapping_result import mapping_result
from show_vacancies_hh import show_hh_vacancies_info
from show_vacancies_superjob import show_sj_vacancies_info


if __name__ == '__main__':
	load_dotenv()

	superjob_api = os.getenv('API_SUPERJOB')

	show_hh_vacancies_info()
	show_sj_vacancies_info(superjob_api)