# Test script for average() function

from a01_aFunction import average

print("=" * 60)
print("Testing average(aList) function")
print("=" * 60)

# Test 1: Simple numeric list
test1 = [1, 2, 3, 4, 5]
result1 = average(test1)
print(f"\nTest 1: {test1}")
print(f"Expected: 3.0, Got: {result1}")
assert result1 == 3.0, "Test 1 failed"

# Test 2: Mixed list with strings
test2 = [10, 'hello', 20, 'world', 30]
result2 = average(test2)
print(f"\nTest 2: {test2}")
print(f"Expected: 20.0 (average of 10, 20, 30), Got: {result2}")
assert result2 == 20.0, "Test 2 failed"
