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
            power = int(str[i][2])
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


req, leq = parse()
print(req)
print(leq)
