def saudacao():
    print("Olá, espero que esteja tudo bem!")

saudacao()

def apresentar(nome, idade):
    print(f"Nome: {nome}, Idade: {idade}")

apresentar("Nuno", 25)

def soma(a, b):
    return a + b

resultado = soma(5, 7)
print("Soma =", resultado)

def teste():
    x = 10
    print("x dentro da função =", x)

teste()
print(x)  # DEMONSTRAÇÃO DO ERRO

def mensagem(txt="Hip! Hip!"):
    print(txt)

mensagem()
mensagem("Hooray!")
