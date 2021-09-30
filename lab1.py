# calculator.py

def sum(m, n):
	if n < 0:
		for i in range(abs(n)):
			m -= 1
	else:
		for i in range(n):
			m += 1
	return m


def divide(m, n):

	if n == 0:
		raise ZeroDivisionError("division by zero!")

	count = 0
	sgn = 1

	if m < 0 and n < 0:
		m = abs(m)
		n = abs(n)
	elif m < 0 and n > 0:
		m = abs(m)
		sgn = -1
	elif m > 0 and n < 0:
		n = abs(n)
		sgn = -1

	while(m > 0):
		m -= n
		count += 1

	if m == 0:
		return sgn * count
	else:
		return sgn * (count - 1)


print(sum(10,5))

print(divide(-10,0))



#note to self:
#this was the cleanest way for divide()
	result = 0
	negRes = m < 0 and n > 0 or m < 0 and n < 0
	m = abs(m)
	n = abs(n)

	while (m - n >= 0):
		m -=n
		result += 1

	result = -result if negRes else result
	return result

#remember to:
# add some comments
# check for inputs types
# 