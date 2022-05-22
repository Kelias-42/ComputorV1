import sys
import numpy as np

def absolute(number):
	return number if number >= 0 else -number

def round_float(number, decimal_count):
	number = float(number)
	string_number = str(number)
	if "." in string_number:
		integer_part, decimal_part = string_number.split(".")[0], string_number.split(".")[1]
		if len(decimal_part) > decimal_count:
			if int(decimal_part[decimal_count]) < decimal_count - 1:
				decimal_part = decimal_part[0:decimal_count]
			else:
				decimal_part = str(int(decimal_part[0:decimal_count]) + 1)
			number = float(integer_part + "." + decimal_part)
	return number

def sqrt(number):
	estimate = number / 2
	while absolute(estimate * estimate - number) > 0.00001:
			estimate = (estimate + number / estimate) / 2
	return round_float(estimate, 6)

def get_highest_power(equation):
	power = 0
	equation = equation.split(' ')
	for i in range(len(equation)):
		if len(equation[i]) > 2 and equation[i][0] == 'X' and equation[i][1] == '^' and int(equation[i][2:]) > power:
			power = int(equation[i][2:])
	return power

def split_coefs(equation, list_len ):
	eq = np.zeros(list_len)
	equation = equation.split(' ')
	sign, power, coef = [1, -1, -1]
	for i in range(len(equation)):
		if (equation[i][0]) == '-':
			if len(equation[i]) == 1:
				sign = -1
			else:
				coef = float(equation[i])
		elif (equation[i][0] == 'X' and equation[i][1] == '^'):
			power = int(equation[i][2:])
		elif ((equation[i][0] >= '0' and equation[i][0] <= '9') or equation[i][0] == '.'):
			coef = float(equation[i])
		if (power != -1 and coef != -1):
			eq[power] = coef * sign
			sign, power, coef = [1, -1, -1]
	return eq

def parse():
	if (len(sys.argv) == 1):
		sys.exit('Please provide a valid equation to solve')
	left, right = (sys.argv[1]).split(" = ")
	max_pwr = max(get_highest_power(left), get_highest_power(right))
	left_equation = split_coefs(left, max_pwr + 1)
	right_equation = split_coefs(right, max_pwr + 1)
	return left_equation, right_equation

def print_reduced_eq(equation):
	print("Reduced form: ", end='')
	for i in range(len(equation)):
		coef = equation[i]
		if coef != 0:
			coef = coef if i == 0 else absolute(coef)
			coef = coef if coef - int(coef) > 0 else int(coef) 
			print(coef, "*", "X^" + str(i), end='')
			if i != len(equation) - 1:
				print(" + " if equation[i + 1] > 0 else " - ", end='')
	print(" = 0")

def compute_delta(a, b, c):
	return b * b - 4 * a * c

def get_coeffs(equation):
	while len(equation) < 3:
		equation.append(0)
	return equation[0], equation[1], equation[2]

def solve(a, b, delta):
	if delta == 0:
		return [-b / (2 * a)]
	elif delta > 0:
		return [(-b + sqrt(delta)) / (2 * a), (-b - sqrt(delta)) / (2 * a)]
	else:
		return [f"{-b} + i * {sqrt(absolute(delta))} / {2 * a}", f"{-b} - i * {sqrt(absolute(delta))} / {2 * a}"]

def pretty_print_solution(delta, sol):
	if delta == 0:
		print("Discrimant is null, ", end='')
	elif delta > 0:
		print("Discriminant is stricly positive, ", end='')
	elif delta < 0:
		print("Discriminant is stricly negative, ", end='')
	print(f"solution{'s are' if len(sol) > 1 else ' is'}:")
	for solution in sol:
		if delta < 0:
			print(solution)
		else:
			print(round_float(solution, 6))

if __name__ == "__main__":
	try:
		req, leq = parse()
		reduced_form = []
		for i in range(len(req)):
			reduced_form.append(req[i] - leq[i])
		if reduced_form == np.zeros(len(reduced_form)).tolist():
			sys.exit("The solution is all real numbers.")
		while reduced_form[-1] == 0:
			reduced_form.pop(-1)
		print_reduced_eq(reduced_form)
		polynomial_degree = len(reduced_form) - 1
		print("Polynomial degree:", polynomial_degree)
		if polynomial_degree > 2:
			print("The polynomial degree is strictly greater than 2, I can't solve.")
		elif polynomial_degree == 0:
			print("No solution")
		elif polynomial_degree == 1:
			c, b, a = get_coeffs(reduced_form)
			solution = -c / b
			if solution == -0:
				solution = 0
			print(f"The solution is\n{round_float(solution, 6)}")
		else:
			c, b, a = get_coeffs(reduced_form)
			delta = compute_delta(a, b, c)
			solution = solve(a, b, delta)
			pretty_print_solution(delta, solution)
	except Exception as ex:
		print(ex)
		print("Please enter your coefficients in the format : C * X^P")
		print("Example of a correct input : '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0'")