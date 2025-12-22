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
# EXERCISE 7.b) - extended class with new method
#__________________________________________________________________________
print( "\n\n=== EXERCISE 7.b) - Extended class with new method ===" )

def c_extended( v=0 ):
   def s_m( x ):
      if x == 1:
         def m( y ): return y**2 + v
      elif x == 2:
         def m( y ): return "< " + str(y) + " >" + "$ " + str(v) + " $"
      elif x == 3:  # NEW METHOD: returns cube
         def m( y ): return y**3 + v
      elif x == 4:  # ANOTHER NEW METHOD: returns factorial
         def m( y ):
            factorial = 1
            for i in range(1, y + 1):
               factorial *= i
            return factorial + v
      elif x == 5:  # ANOTHER NEW METHOD: string concatenation
         def m( y ): return str(v) + " concatenated with " + str(y)
      else:
         def m(): return "---"
      return m
   return s_m

print( "new method (3 - cube):" )
print( "c_extended()( 3 )( 5 ) =", c_extended()( 3 )( 5 ) )  # 125
print( "c_extended( 10 )( 3 )( 2 ) =", c_extended( 10 )( 3 )( 2 ) )  # 18

print( "\nnew method (4 - factorial):" )
print( "c_extended()( 4 )( 5 ) =", c_extended()( 4 )( 5 ) )  # 120
print( "c_extended( 10 )( 4 )( 4 ) =", c_extended( 10 )( 4 )( 4 ) )  # 34

print( "\nnew method (5 - string concatenation):" )
print( "c_extended( 'Hello' )( 5 )( 'World' ) =", c_extended( 'Hello' )( 5 )( 'World' ) )
#__________________________________________________________________________


#__________________________________________________________________________
# EXERCISE 7.c) - meta-class concept (extended)
#__________________________________________________________________________
print( "\n\n=== EXERCISE 7.c) - Meta-class concept (extended) ===" )

def meta_class( class_type="math" ):
   """
   Meta-class: a function that returns classes (functions).
   The meta-class is a class whose methods are classes.
   """
   if class_type == "math":
      def math_class( v=0 ):
         def s_m( x ):
            if x == 1:
               def m( y ): return y + v  # addition
            elif x == 2:
               def m( y ): return y * v if v != 0 else y  # multiplication
            elif x == 3:
               def m( y ): return y - v  # subtraction
            elif x == 4:
               def m( y ): return y / v if v != 0 else "Division by zero"  # division
            else:
               def m(): return "Unknown math operation"
            return m
         return s_m
      return math_class
   
   elif class_type == "string":
      def string_class( v="" ):
         def s_m( x ):
            if x == 1:
               def m( y ): return str(v) + str(y)  # concatenation
            elif x == 2:
               def m( y ): return str(v).upper() + " | " + str(y).upper()  # uppercase
            elif x == 3:
               def m( y ): return str(v).lower() + " | " + str(y).lower()  # lowercase
            else:
               def m(): return "Unknown string operation"
            return m
         return s_m
      return string_class
   
   elif class_type == "geometry":
      def geometry_class( v=0 ):
         def s_m( x ):
            if x == 1:
               def m( y ): return 3.14159 * (v ** 2)  # circle area (v = radius)
            elif x == 2:
               def m( y ): return v * y  # rectangle area
            elif x == 3:
               def m( y ): return (v * y) / 2  # triangle area
            else:
               def m(): return "Unknown geometry operation"
            return m
         return s_m
      return geometry_class
   
   else:
      return c  # default

print( "Math class via meta_class:" )
MathClass = meta_class( "math" )
print( "MathClass( 10 )( 1 )( 5 ) [add] =", MathClass( 10 )( 1 )( 5 ) )  # 15
print( "MathClass( 10 )( 2 )( 5 ) [mul] =", MathClass( 10 )( 2 )( 5 ) )  # 50
print( "MathClass( 10 )( 3 )( 5 ) [sub] =", MathClass( 10 )( 3 )( 5 ) )  # -5
print( "MathClass( 10 )( 4 )( 100 ) [div] =", MathClass( 10 )( 4 )( 100 ) )  # 10.0

print( "\nString class via meta_class:" )
StringClass = meta_class( "string" )
print( "StringClass( 'Hello' )( 1 )( ' World' ) =", StringClass( 'Hello' )( 1 )( ' World' ) )
print( "StringClass( 'Hello' )( 2 )( 'World' ) =", StringClass( 'Hello' )( 2 )( 'World' ) )

print( "\nGeometry class via meta_class:" )
GeometryClass = meta_class( "geometry" )
print( "GeometryClass( 5 )( 1 )( None ) [circle area] =", GeometryClass( 5 )( 1 )( None ) )  # ~78.54
print( "GeometryClass( 5 )( 2 )( 10 ) [rectangle area] =", GeometryClass( 5 )( 2 )( 10 ) )  # 50
print( "GeometryClass( 5 )( 3 )( 10 ) [triangle area] =", GeometryClass( 5 )( 3 )( 10 ) )  # 25.0
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
# EXERCISE 7.d) - decorator variations (expanded)
#__________________________________________________________________________
print( "\n\n=== EXERCISE 7.d) - Decorator variations (expanded) ===" )

print( "\n1. Original order @f @g:" )
@f
@g
def h_original():
   return "h"
print( "Result:", h_original() )
print( "Explanation: f(g(h)) = < # h # >" )

print( "\n2. Reversed order @g @f:" )
@g
@f
def h_var1():
   return "h"
print( "Result:", h_var1() )
print( "Explanation: g(f(h)) = # < h > #" )

print( "\n3. Multiple @f @f @f @g:" )
@f
@f
@f
@g
def h_var2():
   return "h"
print( "Result:", h_var2() )
print( "Explanation: f(f(f(g(h)))) = < < < # h # > > >" )

print( "\n4. Multiple @g @g @g @f:" )
@g
@g
@g
@f
def h_var3():
   return "h"
print( "Result:", h_var3() )
print( "Explanation: g(g(g(f(h)))) = # # # < h > # # #" )

print( "\n5. Alternating @f @g @f @g:" )
@f
@g
@f
@g
def h_var4():
   return "h"
print( "Result:", h_var4() )
print( "Explanation: f(g(f(g(h)))) = < # < # h # > # >" )

print( "\n6. Only @f (no @g):" )
@f
def h_var5():
   return "h"
print( "Result:", h_var5() )
print( "Explanation: f(h) = < h >" )

print( "\n7. Only @g (no @f):" )
@g
def h_var6():
   return "h"
print( "Result:", h_var6() )
print( "Explanation: g(h) = # h #" )

print( "\n8. Custom variation @g @f @f @g @g:" )
@g
@f
@f
@g
@g
def h_var7():
   return "h"
print( "Result:", h_var7() )
print( "Explanation: g(f(f(g(g(h))))) = # < < # # h # # > > #" )
