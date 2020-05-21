import sys

def split_coeffs(str):
    eq = [0, 0, 0]
    str = str.split(' ')
    sign, power, coef = [1, -1, -1]
    for i in range(len(str)):
        if (str[i][0]) == '-':
            if len(str[i]) == 1:
                sign = -1
            else:
                coef = float(str[i])
        elif (str[i][0] == 'X'):
            power = int(str[i][2:])
            if power > 2:
                sys.exit('The polynomial degree is strictly greater than 2, I can\'t solve.')
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
    leq = split_coeffs(left)
    req = split_coeffs(right)
    return leq, req

def print_eq(eq):
    if (eq == [0, 0, 0]):
        sys.exit("The solution is all real numbers.")
    for i in range(3):
        if eq[i] == 0:
            pass

req, leq = parse()
reduced_form = [req[0] - leq[0], req[1] - leq[1], req[2] - leq[2]]
print_eq(reduced_form)
print(req)
print(leq)
