import sys
import numpy as np

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
		sys.exit('Please provide valid equation to solve')
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
	if eq == np.zeros(len(eq)).tolist():
		sys.exit("The solution is all real numbers.")
	print("Reduced form: ", end='')
	for i in range(len(eq)):
		coef = eq[i]
		if coef != 0:
			coef = coef if i == 0 else abs(coef)
			coef = coef if coef - int(coef) > 0 else int(coef) 
			print(coef, "*", "X^" + str(i), end='')
			if i != len(eq) - 1 and not is_at_end(eq, i + 1):
				print(" + " if eq[i + 1] > 0 else " - ", end='')
	print(" = 0")

if __name__ == "__main__":
	req, leq = parse()
	reduced_form = []
	for i in range(len(req)):
		reduced_form.append(req[i] - leq[i])
	print_reduced_eq(reduced_form)
	
	#sys.exit('The polynomial degree is strictly greater than 2, I can\'t solve.')
