import math

def isprime(x):
	for i in range(2,int(math.sqrt(x))):
		if x%i == 0:
			return False
	return True

print(isprime(3001))