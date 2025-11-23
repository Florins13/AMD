lista = [1, 2, 3]
tuplo = tuple(lista)
print("Tuplo:", tuplo)

tuplo2 = (10, 20, 30)
lista2 = list(tuplo2)
print("Lista:", lista2)

pares = [("a", 1), ("b", 2), ("c", 3)]
d = dict(pares)
print("Dicionário:", d)

print(list(d.keys()))
print(list(d.values()))
print(list(d.items()))

quadrados = [x*x for x in range(1, 6)]
print(quadrados)

pares = [x for x in range(10) if x % 2 == 0]
print(pares)

nomes = ["florin", "diogo", "nuno"]
maiusculas = [nome.upper() for nome in nomes]
print(maiusculas)

tuplos = [(x, x**2) for x in range(5)]
print(tuplos)
