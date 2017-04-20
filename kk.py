# the following command will remove all the .txt files
# find . -name "*.txt" -type f -delete
import sys
import random
import math
import timeit

def kk(A):
	while len(A) > 1:
		largest = max(A)
		A.remove(largest)
		second_largest = max(A)
		A.remove(second_largest)
		A.append(largest - second_largest)
	return A[0]

num_set = []
input_file = open(sys.argv[1], 'r')
for line in input_file:
	e = int(line)
	num_set.append(e)

start = timeit.default_timer()
output = kk(num_set)
end = timeit.default_timer()
time = end - start
# print "%s; Time in seconds: %s" % (output, time)
print output