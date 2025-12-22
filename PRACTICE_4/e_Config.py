# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
# version: v06
# ===============================



#______________________________________________________________________________
# The modules to import
import os
import sys
from getopt import getopt, error
# The "getopt" module helps scripts to parse the command line arguments in sys.argv.
# It supports the same conventions as the Unix getopt() function
# (including the special meanings of arguments of the form �-� and �--�).




#______________________________________________________________________________
# A class that parses the command line argunmets
# In this example the system has 3 parameters (a, b, c)
# each parameter has a default value that can be redefined as a command line option
class e_Config():
   def __init__( self ):
      # definition of default (option, value) pairs
      # i.e., the defualt values for the system parameters: x, y, z, t
      self.__optionValue = { \
         ("-x", "--paramX"): "valueX", \
         ("-y", "--paramY"): 100, \
         ("-z", "--paramZ"): "valueZ", \
         ("-t", "--paramT"): 999 }


#______________________________________________________________________________
# Exercise 6.e) - Backup Config using command-line pattern
import time

class BackupConfig():
   def __init__( self ):
      # definition of default (option, value) pairs for backup
      self.__optionValue = { \
         ("-s", "--sources"): "./python/a01_aFunction.py,./python/a02_anotherBehavior.py", \
         ("-d", "--target"): "./backups", \
         ("-v", "--version"): "1", \
         ("-c", "--comment"): "" }
  
   def config( self, argv ):
      try:
         try:
            (argv_optionValue, args) = \
               getopt( argv[1:], \
                       "s:d:v:c:", \
                       ["sources=", "target=", "version=", "comment="] )
         except error: raise Usage( self.usage() )
      except Usage as incorrect:
         sys.stderr.write( incorrect.msg )
         sys.exit( 2 )
         
      list_optionName = self.__optionValue.keys()
      for (option, value) in argv_optionValue:
         for optionName in list_optionName:
            if option in optionName: self.__optionValue[ optionName ] = value

   def get_sources( self ):
      sources_str = self.__optionValue[("-s", "--sources")]
      return [s.strip() for s in sources_str.split(",")]
   
   def get_target( self ):
      return self.__optionValue[("-d", "--target")]
   
   def get_version( self ):
      return self.__optionValue[("-v", "--version")]
   
   def get_comment( self ):
      return self.__optionValue[("-c", "--comment")]

   def usage( self ):
      thisFile = os.path.basename( sys.argv[0] )
      aStr = ""
      aStr += "\n" + "Backup Usage:"
      aStr += "\n" + "> " + thisFile + " -s <sources> -d <target> -v <version> [-c <comment>]"
      aStr += "\n" + "or"
      aStr += "\n" + "> " + thisFile + " --sources <sources> --target <target> --version <version> [--comment <comment>]"
      aStr += "\n" + "Parameters:"
      aStr += "\n" + "  -s, --sources : Comma-separated list of files/folders"
      aStr += "\n" + "  -d, --target  : Target directory for backup"
      aStr += "\n" + "  -v, --version : Backup version (1, 2, or 3)"
      aStr += "\n" + "  -c, --comment : Optional comment (for version 3)"
      aStr += "\n"
      return aStr

def backup_v01(sources, target_dir):
   hoje = time.strftime('%Y%m%d%H%M%S')
   zipname = os.path.join(target_dir, hoje + '.zip')
   if not os.path.exists(target_dir): os.makedirs(target_dir)
   command = "zip -r {0} {1}".format(zipname, " ".join(sources))
   print("\n[backup_v01] Comando: " + command)

def backup_v02(sources, target_dir):
   dia = time.strftime('%Y%m%d')
   destino_dia = os.path.join(target_dir, dia)
   if not os.path.exists(destino_dia): os.makedirs(destino_dia)
   hora = time.strftime('%H%M%S')
   zipname = os.path.join(destino_dia, hora + '.zip')
   command = "zip -r {0} {1}".format(zipname, " ".join(sources))
   print("\n[backup_v02] Comando: " + command)

def backup_v03(sources, target_dir, comentario=""):
   dia = time.strftime('%Y%m%d')
   destino_dia = os.path.join(target_dir, dia)
   if not os.path.exists(destino_dia): os.makedirs(destino_dia)
   hora = time.strftime('%H%M%S')
   if comentario:
      comentario = comentario.replace(" ", "_")
      zipname = os.path.join(destino_dia, "{0}_{1}.zip".format(hora, comentario))
   else:
      zipname = os.path.join(destino_dia, hora + '.zip')
   command = "zip -r {0} {1}".format(zipname, " ".join(sources))
   print("\n[backup_v03] Comando: " + command)

  
   def config( self, argv ):
      try:
         try:
            (argv_optionValue, args) = \
               getopt( argv[1:], \
                       "x:y:z:t:", \
                       ["paramX=", "paramY=", "paramZ=", "paramT="] )
         except error: raise Usage( self.usage() )
      except Usage as incorrect:
         sys.stderr.write( incorrect.msg )
         sys.exit( 2 )
         
      list_optionName = self.__optionValue.keys()
      for (option, value) in argv_optionValue:
         for optionName in list_optionName:
            if option in optionName: self.__optionValue[ optionName ] = value


   def obterOpcaoValor( self ):
      resultado = {}
      for parOpcao in self.__optionValue.keys():
         resultado[ parOpcao[ 0 ] ] = self.__optionValue[ parOpcao ]
      return list( resultado.items() )
   

   def usage( self ):
      thisFile = os.path.basename( sys.argv[0] )
      aStr = ""
      aStr += "\n"
      aStr += "\n" + "Usage:"
      aStr += "\n" +  "> " + thisFile + " -x valueX -y valueY -z valueZ -t valueT"
      aStr += "\n" +  "or"
      aStr += "\n" +  "> " + thisFile + " --paramX valueX --paramY valueY --paramZ valueZ --paramT valueT"
      aStr += "\n"
      return aStr




#______________________________________________________________________________
# Utility Class
#(explores exceptions and decorators such as "getter" and "setter")
class Usage( Exception ):
   def __init__( self, msg ):
      self.msg = msg

   @property
   def msg( self ): return self.__msg

   @msg.setter
   def msg( self, value ):
      assert isinstance( value, str ), "PTS | msg: string expected"
      self.__msg = value
      
   @msg.deleter
   def msg( self ): self.__msg = ""




#______________________________________________________________________________
# The "main" of this module (is case this module is loaded from another module)
if __name__ == "__main__":
   # Original test
   # e = e_Config()
   # e.config( sys.argv )
   # print( e.obterOpcaoValor() )
   
   # a test: uncomment the next 3 lines to activate the test
   # argvTest = ["f", '-x', 111, '-y', 222, '-z', 333, '-t', 444]
   # e.config( argvTest )
   # print( e.obterOpcaoValor() )
   
   # Exercise 6.e) - Backup with command-line pattern
   print("\n" + "="*60)
   print("BACKUP COM COMMAND-LINE PATTERN (Exercise 6.e)")
   print("="*60)
   
   config = BackupConfig()
   config.config( sys.argv )
   
   sources = config.get_sources()
   target = config.get_target()
   version = config.get_version()
   comment = config.get_comment()
   
   print("Sources: " + str(sources))
   print("Target: " + target)
   print("Version: " + version)
   if comment: print("Comment: " + comment)
   print("="*60)
   
   if version == "1":
      backup_v01(sources, target)
   elif version == "2":
      backup_v02(sources, target)
   elif version == "3":
      backup_v03(sources, target, comment)
   else:
      print("\nERRO: Versão inválida. Use 1, 2 ou 3.")
      sys.exit(1)
   
   print("\n" + "="*60)
   print("BACKUP CONCLUÍDO!")
   print("="*60 + "\n")






