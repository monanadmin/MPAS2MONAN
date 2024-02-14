"""domainVariables.py
   Description: This python script write core_variables.inc
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def core_variables_write(registry_processed, inc_dir):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   model = root.attrib["model"]
   version = root.attrib["version"]
   core = root.attrib["core"]
   #abrev = root.attrib["core_abbrev"]
   exe_name = "monan"
   git_ver = "0.1.0"
   build_target = "gfortran"

   #fd3 = open(inc_dir+"/modCoreVariables.f90","w")
   fd3 = open(inc_dir+"/core_variables.inc", "w")
   #fd3.write("module modCoreVariables\n\n")
   fd3.write("       core % modelName = '{1}'\n"     .format(core,model));
   fd3.write("       core % coreName = '{1}'\n"      .format(core,core));
   fd3.write("       core % modelVersion = '{1}'\n"  .format(core,version));
   fd3.write("       core % executableName = '{1}'\n".format(core,exe_name));
   fd3.write("       core % git_version = '{1}'\n"   .format(core,git_ver));
   fd3.write("       core % build_target = '{1}'\n"  .format(core,build_target));
   #fd3.write("end module modCoreVariables\n")
   fd3.close()
   return