# to use accented characters in the code
# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
#____________________
# Python Crash-Course
# ===============================



# Assignment
# ==========
#> As a programmer, assignment and types should not be surprising to you!

# Strings
#> notice how you can access characters in the string using array syntax
def hello_function():
   data = 'hello world'
   print( data[0] )
   print( len(data) )
   print( data )

# Numbers
def number_function():
   value = 123.1
   print( value )
   value = 10
   print( value )

# Boolean
def boolean_section():
   a = True
   b = False
   print( a, b )

# Multiple Assignment
#> This can also be very handy for unpacking data in simple data structures
def multiple_assignments():
   a, b, c = 1, 2, 3
   print( a, b, c )

# No value
def no_value():
   a = None
   print(a)


# Flow Control
# ============
#> There are three main types of flow control that you need to learn:
#> If-Then-Else conditions, For-Loops and While-Loops

# If-Then-Else
def if_then_else():
   value =60
   if value < 60:
      print( 'That is safe' )
   elif value < 120:
      print( 'That is fast' )
   else:
      print( 'That is too fast' )

def for_loop():
   # For-Loop
   for i in range(10):
      print(i)

def while_loop():
   # While-Loop
   i = 0
   while i < 10:
      print( i )
      i += 1


# Data Structures
# ===============
#> There are three data structures in Python that you will find the most used and useful.
#> They are tuples, lists and dictionaries

# Tuple (cannot change - immutable)
#> read-only collections of items
def my_tuples():
   a = (1, 2, 3)
   print( a )


# Lists
#> use the square bracket notation and can be indexed using array notation
#> Notice that we are using some simple printf-like
#> functionality to combine strings and variables when printing
def my_list():
   mylist = [1, 2, 3]
   print( "Zeroth Value: %d" % mylist[0] )
   mylist.append(4)
   print( "List Length: %d" % len(mylist) )
   for value in mylist:
      print( value )


# Dictionaries
#> mappings of names to values, like key-value pairs
#> Note the use of the curly bracket, and
#> colon notations when defining the dictionary
def my_dict():
   mydict = {'a': 1, 'b': 2, 'c': 3}
   print( "A value: %d" % mydict['a'] )
   mydict['a'] = 11
   print( "A value: %d" % mydict['a'] )
   print( "Keys: %s" % mydict.keys() )
   print( "Values: %s" % mydict.values() )
   for key in mydict.keys():
      print( mydict[key] )


# Functions
# ===========
#> The biggest gotcha with Python is the whitespace
#> Ensure that you have an empty new line after indented code

# Sum function
def my_sum(x, y):
   return x + y

# Test sum function
x = my_sum( 1000, 3333 )
print( x )

# A function that is called in case this file is not being imported
def main():
   my_sum( 2, 4 )
   my_dict()
   my_list()
   my_tuples()
   while_loop()
   for_loop()
   if_then_else()
   hello_function()
   number_function()
   boolean_section()
   multiple_assignments()
   no_value()


#_______________________________________________________________________________
# the starting point whenever this file is not being imported (from another)
if __name__=="__main__":
   main()


