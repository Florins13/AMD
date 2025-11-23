import modulo_util

modulo_util.saudacao("Florin")
print(modulo_util.soma(3, 4))

import modulo_util as mu
print(mu.dobro(10))

from modulo_util import soma
print(soma(100, 200))

from modulo_util import saudacao, dobro
saudacao("Diogo")
print(dobro(7))