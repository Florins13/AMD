lista = [1, 2, 3, 4]

print(lista)
print(lista[0])
print(lista[-1])

lista[1] = 8
print(lista)

lista.append(5)
lista.insert(0, "zero")
print(lista)

del lista[0]
lista.pop()
lista.remove(8)
print(lista)

lista2 = ["abc", "def"]
resultado = lista + lista2
print(resultado)

print(len(resultado))

print("abc" in resultado)