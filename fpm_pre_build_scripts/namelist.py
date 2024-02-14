"""namelist.py
   Description: This python script namelist
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def namelist_write(fileName):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(fileName)
   root = tree.getroot()

   core = root.attrib["core"]

   sectors = ["nhyd_model", "damping", "limited_area", "io", "decomposition", "restart", "printout",
            "IAU", "physics", "assimilation", "development","soundings"  ]

   namelist = open("namelist.{0}".format(core), "w")

   for child in root:
      if child.tag == "nml_record" and child.attrib["in_defaults"] == "true":
         if child.attrib["name"] in sectors: #Se existe o setor do namelist na lista de setores
            namelist.write("&{0}\n".format(child.attrib["name"]))
            for gran_child in child:
               """Se for uma tag de namelist, nml_option, então os elementos devem ser percorridos"""
               if gran_child.tag == "nml_option":
                  if "in_defaults" in gran_child.attrib:
                     """Verifica se o in_defaults não é falso"""
                     if gran_child.attrib["in_defaults"] != "false":
                        """O trecho abaixo preenche o namelist com suas variáveis e valores:"""
                        if gran_child.attrib["type"] == "character":
                           """Se o tipo da variável for string é preciso acrescentar aspas antes e depois dos valores"""
                           namelist.write("   {0} = '{1}'\n".format(gran_child.attrib["name"],gran_child.attrib["default_value"]))
                        else:
                           namelist.write("   {0} = {1}\n".format(gran_child.attrib["name"],gran_child.attrib["default_value"]))
                  else:
                     """O trecho abaixo preenche o namelist com suas variáveis e valores:"""
                     if gran_child.attrib["type"] == "character":
                        """Se o tipo da variável for string é preciso acrescentar aspas antes e depois dos valores"""
                        namelist.write("   {0} = '{1}'\n".format(gran_child.attrib["name"],gran_child.attrib["default_value"]))
                     else:
                        namelist.write("   {0} = {1}\n".format(gran_child.attrib["name"],gran_child.attrib["default_value"]))
            namelist.write("/\n")

   namelist.close()