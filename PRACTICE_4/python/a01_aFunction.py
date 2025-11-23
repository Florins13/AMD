# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
# version: v06
# ===============================



def f( a_list ):
   a_list = [ str(x).upper() for x in a_list if isinstance(x, int) and x % 2 == 0 ]
   while True:
      v = input( '? > ' )
      if v.upper() in a_list or v == 'quit' or v == 'exit': break
      print( v.upper() )


if __name__ == "__main__":
   a_list = [ 'o', 1, 33, 'hello' ] # PARA 3 PRIMEIROS TESTES NO TERMINAL
   #a_list = [ 'o', 2, 33, 'hello' ] # PARA ÚLTIMO TESTE NO TERMINAL
   f( a_list )



