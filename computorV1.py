import sys
import numpy as np

def absolute(number):
	return number if number > 0 else -number

def sqrt(number):
        estimate = number / 2
        while absolute(estimate * estimate - number) > 0.00001:
                estimate = (estimate + number / estimate) / 2
        return estimate

def get_highest_power(str):
	power = 0
	str = str.split(' ')
	for i in range(len(str)):
		if len(str[i]) > 2 and str[i][0] == 'X' and str[i][1] == '^' and int(str[i][2:]) > power:
			power = int(str[i][2:])
	return power

def split_coefs(str, list_len ):
	eq = np.zeros(list_len)
	str = str.split(' ')
	sign, power, coef = [1, -1, -1]
	for i in range(len(str)):
		if (str[i][0]) == '-':
			if len(str[i]) == 1:
				sign = -1
			else:
				coef = float(str[i])
		elif (str[i][0] == 'X' and str[i][1] == '^'):
			power = int(str[i][2:])
		elif ((str[i][0] >= '0' and str[i][0] <= '9') or str[i][0] == '.'):
			coef = float(str[i])
		if (power != -1 and coef != -1):
			eq[power] = coef * sign
			sign, power, coef = [1, -1, -1]
	return eq

def parse():
	if (len(sys.argv) == 1):
		sys.exit('Please provide a valid equation to solve')
	left, right = (sys.argv[1]).split(" = ")
	max_pwr = max(get_highest_power(left), get_highest_power(right))
	leq = split_coefs(left, max_pwr + 1)
	req = split_coefs(right, max_pwr + 1)
	return leq, req

def is_at_end(eq, i):
	while i != len(eq):
		if eq[i] != 0:
			return False	
		i += 1
	return True

def print_reduced_eq(eq):
	print("Reduced form: ", end='')
	for i in range(len(eq)):
		coef = eq[i]
		if coef != 0:
			coef = coef if i == 0 else absolute(coef)
			coef = coef if coef - int(coef) > 0 else int(coef) 
			print(coef, "*", "X^" + str(i), end='')
			if i != len(eq) - 1:
				print(" + " if eq[i + 1] > 0 else " - ", end='')
	print(" = 0")

def compute_delta(a, b, c):
	return b * b - 4 * a * c

def get_coeffs(equation):
	while len(equation) < 3:
		equation.append(0)
	return equation[0], equation[1], equation[2]

def solve(a, b, delta):
	if delta == 0:
		return -b / 2 * a
	elif delta > 0:
		return [(-b + sqrt(delta)) / 2 * a, (-b - sqrt(delta)) / 2 * a]
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
		print("{:.6f}".format(solution))


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
		print("Polynomial degree:", len(reduced_form) - 1)
		if len(reduced_form) - 1 > 2:
			print("The polynomial degree is strictly greater than 2, I can't solve.")
		else:
			a, b, c = get_coeffs(reduced_form)
			delta = compute_delta(a, b, c)
			sol = solve(a, b, delta)
		pretty_print_solution(delta, sol)
	except Exception as ex:
		print(ex)
		print("Please enter your coefficients in the format : C * X^P")
		print("Example of a correct input : '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0'")