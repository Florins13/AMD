# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
# version: v06
# ===============================



print( "\n----- One Example -----" )

def f( v="oneParameter" ):
   def g(): return v
   return g

x = f()
print( x )
print( x() )



print( "\n----- Another Example -----" )

def f( v1="oneParameter" ):
   def g( v2="anotherParameter" ):
      def h(): return v1 + "//" + v2
      return h
   return g

x = f()
print( x )
print( x() )
print( x()() )
print( f( "http:" )( "www" )() )



#__________________________________________________________________________
# Preliminary experiments (to support the understanding of @decorator)
# a function that returns another function; remarks:
# - the variable v exists in the scope of the local functions
# INPORTANT:
# this construction enables to formulate the notion of "class", where:
# - c, is a class
# - s_m, is the scope of the methods
# - m, is a method
#__________________________________________________________________________
def c( v=0 ):
   def s_m( x ):
      if x == 1:
         def m( y ): return y**2 + v
      elif x == 2:
         def m( y ): return "< " + str(y) + " >" + "$ " + str(v) + " $"
      else:
         def m(): return "---"
      return m
   return s_m

print( "\nPreliminary experiments (function that returns a function):" )
o = c()
# note that o is a function
print( o( 1 ) )
print()
o1 = o( 1 )
print( o1( 100 ) )
print( o( 2 )( "ola" ) )
print( o( 3 )() )
# OR
print( c()( 1 )( 100 ) )
print( c( "www" )( 2 )( "ola" ) )
print( c()( 3 )() )
#__________________________________________________________________________


#__________________________________________________________________________
# extended class with new method
#__________________________________________________________________________
print( "\n\n=== extended class with new method ===" )

def c_extended( v=0 ):
   def s_m( x ):
      if x == 1:
         def m( y ): return y**2 + v
      elif x == 2:
         def m( y ): return "< " + str(y) + " >" + "$ " + str(v) + " $"
      elif x == 3:  # NEW METHOD: returns cube
         def m( y ): return y**3 + v
      else:
         def m(): return "---"
      return m
   return s_m

print( "new method (3 - cube):" )
print( "c_extended()( 3 )( 5 ) =", c_extended()( 3 )( 5 ) )  # 125
print( "c_extended( 10 )( 3 )( 2 ) =", c_extended( 10 )( 3 )( 2 ) )  # 18
#__________________________________________________________________________


#__________________________________________________________________________
# meta-class concept
#__________________________________________________________________________
print( "\n===  meta-class concept ===" )

def meta_class( class_type="math" ):
   if class_type == "math":
      def math_class( v=0 ):
         def s_m( x ):
            if x == 1:
               def m( y ): return y + v  # addition
            elif x == 2:
               def m( y ): return y * v if v != 0 else y  # multiplication
            else:
               def m(): return "Unknown"
            return m
         return s_m
      return math_class
   else:
      return c  # default

print( "math class via meta_class:" )
MathClass = meta_class( "math" )
print( "mathClass( 10 )( 1 )( 5 ) [add] =", MathClass( 10 )( 1 )( 5 ) )  # 15
print( "mathClass( 10 )( 2 )( 5 ) [mul] =", MathClass( 10 )( 2 )( 5 ) )  # 50
#__________________________________________________________________________



#__________________________________________________________________________
# seja:
# f( g ( h( x ) ) )
# if we intend to define h as the result of this composition
# i.e., if we intend to do:
# h = f( g ( h ) )
# IMPORTANT: note that h is a function (f o g)
# and not the result of invoking g and f
# then we write
# @f
# @g
# def h(): ...
#
# and, in this case we say that f and g are "decorators" of h
#__________________________________________________________________________

# Example:
def f( fn ):
   def local():
      s = "< " + fn() + " >"
      return s
   return local

def g( fn ):
   def local():
      s = "# " + fn() + " #"
      return s
   return local
   
print( "\nversion with @decorator syntax:" )
@f
@g
def h():
   s = "h"
   return s

print( h() )

print( "\nversion with direct (explicit) definition:" )
def h():
   s = "h"
   return s

h = f( g ( h ) )
print( h() )


#__________________________________________________________________________
# decorator variations
#__________________________________________________________________________
print( "\n\n=== PART (D): decorator variations ===" )

print( "\n1. reversed order @g @f:" )
@g
@f
def h_var1():
   return "h"
print( h_var1() )

print( "\n2. multiple @f @f @f @g:" )
@f
@f
@f
@g
def h_var2():
   return "h"
print( h_var2() )
