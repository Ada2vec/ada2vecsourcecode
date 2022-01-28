import math


def variance(sumvalue, n):
	mean = sumvalue / n
	return (sumvalue * (1 - mean)**2 + (n - sumvalue) * (0 - mean)**2) / n


def hoeffding_bound(t_mean, t_len, t1_mean, t1_len, confidence):
	valueofsum = (t_mean * t_len + t1_mean * t1_len)
	variancevalue = variance(valueofsum, t_len + t1_len)
	harmonic_mean = 1 / ((1 / t_len) + (1 / t1_len))
	delta_prime = math.log(2 / confidence)
	epsilon = (math.sqrt((2 / harmonic_mean) * variancevalue * delta_prime) + (2 / (3 * harmonic_mean) * delta_prime))
	assert(epsilon >= 0)
	return abs(t_mean - t1_mean) < epsilon
