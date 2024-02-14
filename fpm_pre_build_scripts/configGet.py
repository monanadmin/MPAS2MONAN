
"""configDeclare.py
   Description: This python script write config_get.inc
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def config_get(registry_processed, inc_dir):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()
   
   """Abre o arquivo config_get.inc """
   fcg = open(inc_dir+"/modConfigGet.f90", "w")

   fcg.write("module modConfigGet\n\n")
   fcg.write("   contains\n\n")

   for child in root:
      if child.tag == "nml_record":
         for gran_child in child:
            if gran_child.tag == "nml_option":
               fcg.write("      call mpas_pool_get_config(configPool, '{0}', {0})\n".format(gran_child.attrib["name"]))
         fcg.write("\n")

   fcg.write("\n\nend module modConfigGet\n")

   fcg.close()


