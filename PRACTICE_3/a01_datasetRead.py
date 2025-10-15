# # to use accented characters in the code
# # -*- coding: cp1252 -*-
# # ===============================
# # author: Paulo Trigo Silva (PTS)
# # v08 (Python39, Orange3)
# # ===============================
#
#
# #__________________________________________
# # Orange Documentation:
# # http://docs.orange.biolab.si
# #
# # Orange Reference Manual:
# # http://docs.orange.biolab.si/3/data-mining-library/#reference
# #
# # Tutorial:
# # http://docs.orange.biolab.si/3/data-mining-library/#tutorial
# #
# # details about data (attribute+class) characterization:
# # http://docs.orange.biolab.si/3/data-mining-library/tutorial/data.html#data-input
# #__________________________________________
#
# #_______________________________________________________________________________
# # Modules to Evaluate
import sys
from u01_util import my_print
import Orange as DM
#
#
#
# #_______________________________________________________________________________
# # read a "dataset"
# # the file name (that can be passed in the command line)
# fileName = "./_dataset/lenses.tab"
# #fileName = "./_dataset/adult_sample"
# if len( sys.argv ) > 1: fileName = sys.argv[ 1 ]
#
# #try:
# dataset = DM.data.Table( fileName )
# #print(dataset)
# print(f'\r\ndomain {dataset.domain}')
# print(f'\r\nvariables {dataset.domain.variables}')
# print(f'\r\nattributes {dataset.domain.attributes}')
# print(f'\r\nclass_var {dataset.domain.class_var}')
# print(f'\r\ndir {dir(dataset.domain.class_var)}')
# #except:
# #   my_print( "--->>> error - can not open the file: %s" % fileName )
# #   exit()
#
#
#
# #_______________________________________________________________________________
# # variables: name (type = discrete | continuous): [value1, value2, ...]
# # variables, in Orange, refer to features or class
# # cf., http://docs.orange.biolab.si/3/data-mining-library/tutorial/data.html#exploration-of-the-data-domain
# variable_list = dataset.domain.variables
# #variable_list = dataset.domain.attributes
#
# my_print( aStr = ">> %d Variables (attributes+class) <<" % len( variable_list ) )
# print( ">> name (type): (value1, value2, ...) <<" )
#
# nDisc=0; nCont=0; nStr=0;
# for variable in variable_list:
#    print( ":: %s %s" % ( variable.name, variable.TYPE_HEADERS ), end="" ),
#    if variable.is_discrete:
#       print( ": {0} ".format( variable.values ) )
#       #print( variable.values )
#       nDisc += 1
#    elif variable.is_continuous:
#       print()
#       nCont += 1
#    else:
#       nStr += 1
# my_print( ">> Types: %d discrete, %d continuous <<" % ( nDisc, nCont ) )
#
#
#
# #_______________________________________________________________________________
# # Class: name (type = discrete | continuous): <value1, value2, ...>
# the_class = dataset.domain.class_var
# my_print( ">> Class <<" )
# print( ":: %s %s: %s " % ( the_class.name,
#                            the_class.TYPE_HEADERS,
#                            the_class.values ) )
#
#
#
# #_______________________________________________________________________________
# # First N Instances
# N = 20
# my_print( "First %d instances:" % N )
# for i in range( N ): print( dataset[ i ] )

# read dataset
fileName = "./_dataset/lenses.tab"
if len(sys.argv) > 1:
    fileName = sys.argv[1]

try:
    dataset = DM.data.Table(fileName)
except:
    my_print("--->>> error - can not open the file: %s" % fileName)
    exit()

# f) print the dataset
print(dataset)

# g) print dataset.domain
print(dataset.domain)

# h) print dataset.domain.variables
print(dataset.domain.variables)

# i) print dataset.domain.attributes
print(dataset.domain.attributes)

# j) print dataset.domain.class_var
print(dataset.domain.class_var)

# k) print all methods/attributes of dataset.domain.class_var
print(dir(dataset.domain.class_var))

# l) Explore variables vs attributes
# -> dataset.domain.variables includes all variables (predictors + class)
# -> dataset.domain.attributes includes only the predictor variables (excludes the class)
variable_list = dataset.domain.variables
print(">> Variables (attributes + class) <<")
for variable in variable_list:
    print(f":: {variable.name} ({variable.TYPE_HEADERS})", end="")
    if variable.is_discrete:
        print(f": {variable.values}")
    else:
        print()

attribute_list = dataset.domain.attributes
print("\n>> Attributes (predictors only) <<")
for attribute in attribute_list:
    print(f":: {attribute.name} ({attribute.TYPE_HEADERS})", end="")
    if attribute.is_discrete:
        print(f": {attribute.values}")
    else:
        print()
