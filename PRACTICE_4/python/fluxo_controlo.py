x = 10

if x > 10:
    print("maior que 10")
elif x == 10:
    print("igual a 10")
else:
    print("menor que 10")

i = 0
while i < 5:
    print("i vale", i)
    i += 1

for letra in "Python":
    print(letra)

for n in range(10):
    if n == 5:
        break
    print("n:", n)

for n in range(6):
    if n % 2 == 0:
        continue
    print("ímpar:", n)

for n in range(0, 21, 5):
    print("n:", n)