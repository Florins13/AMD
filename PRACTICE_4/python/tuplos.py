t = (1, 2, 3)

print(t)
print(t[0])
print(t[-1])

pessoa = ("Nuno", 25, "Sines")
print(pessoa)

nome, idade, cidade = pessoa
print(nome, idade, cidade)

t[1] = 99 # DEMONSTRAÇÃO DO ERRO

mistura = [ ("a", 1), ("b", 2), ("c", 3) ]
print(mistura)

lista = [1, 2, 3]
tuplo = tuple(lista)
print(tuplo)

lista2 = list(tuplo)
print(lista2)