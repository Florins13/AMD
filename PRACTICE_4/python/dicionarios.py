info = {"nome": "Nuno", "idade": 25, "curso": "MEIC"}

print(info)
print(info["nome"])
print(info["idade"])

info["cidade"] = "Sines"

info["idade"] = 29

del info["curso"]
valor = info.pop("cidade")

print(info.keys())
print(info.values())
print(info.items())

print("nome" in info)
print("clube" in info)

for chave, valor in info.items():
    print(chave, "→", valor)