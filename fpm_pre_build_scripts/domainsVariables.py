"""domainVariables.py
   Description: This python script write domains_variables.inc.inc.
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def domain_variables(registry_processed, inc_dir):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   """Ajustando as informações iniciais do arquivo XML"""
   core = root.attrib["core"]

   #fd4 = open(inc_dir+"/modDomainVariables.f90","w")
   fd4 = open(inc_dir+"/domain_variables.inc","w")
   #fd4.write("module modDomainVariables\n\n")
   fd4.write("       domain % namelist_filename = 'namelist.{0}'\n".format(core))
   fd4.write("       domain % streams_filename = 'streams.{0}'\n".format(core))
   #fd4.write("end module modDomainVariables\n")
   fd4.close()

   return