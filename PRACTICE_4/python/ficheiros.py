f = open("1f.txt", "r")
conteudo = f.read()
print("Conteúdo completo:\n", conteudo)
f.close()

f = open("1f.txt", "r")
for linha in f:
    print("Linha:", linha.strip())
f.close()

with open("1f.txt", "r") as f:
    for linha in f:
        print("WITH:", linha.strip())

with open("novo1f.txt", "w") as f:
    f.write("Primeira linha\n")
    f.write("Segunda linha\n")

with open("novo1f.txt", "a") as f:
    f.write("Linha adicionada\n")

print("\nConteúdo de novo1f.txt:")
with open("novo1f.txt", "r") as f:
    print(f.read())