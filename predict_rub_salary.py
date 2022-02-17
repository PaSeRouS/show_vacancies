def predict_rub_salary(salary_from, salary_to):
	if salary_from and salary_to:
		return (salary_from+salary_to)/2
	elif not salary_from and salary_to:
		return salary_to*0.8
	elif salary_from and not salary_to:
		return salary_from*1.2