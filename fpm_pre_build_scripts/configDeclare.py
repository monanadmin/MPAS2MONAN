
"""configDeclare.py
   Description: This python script write config_declare.inc
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def config_declare(registry_processed, inc_dir):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()
   
   """Abre o arquivo config_declare.inc """
   fcd = open(inc_dir+"/modConfigDeclare.f90", "w")

   fcd.write("module modConfigDeclare\n\n")
   fcd.write("   contains\n\n")

   for child in root:
      if child.tag == "nml_record":
         for gran_child in child:
            if gran_child.tag == "nml_option":
               if gran_child.attrib["type"] == "character":
                  fcd.write("      character (len=StrKIND), pointer :: {0}\n".format(gran_child.attrib["name"]))
               elif gran_child.attrib["type"] == "integer":
                  fcd.write("      integer, pointer :: {0}\n".format(gran_child.attrib["name"]))
               elif gran_child.attrib["type"] == "real":
                  fcd.write("      real (kind=RKIND), pointer :: {0}\n".format(gran_child.attrib["name"]))
               elif gran_child.attrib["type"] == "logical":
                  fcd.write("      logical, pointer :: {0}\n".format(gran_child.attrib["name"]))
         fcd.write("\n")

   fcd.write("\n\nend module modConfigDeclare\n")

   fcd.close()


