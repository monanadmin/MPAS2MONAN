"""namelistCall.py
   Description: This python script namelist_call.inc
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def header_define_packages(fd1,abrev):
   fd1.write("   function {0}_define_packages(packagePool) result(iErr)\n".format(abrev));
   fd1.write("      use mpas_derived_types\n");
   fd1.write("      use mpas_pool_routines\n");
   fd1.write("      use mpas_io_units\n");
   fd1.write("      implicit none\n");
   fd1.write("      type (mpas_pool_type), intent(inout) :: packagePool !< Input: MPAS Pool for containing package logicals.\n\n");
   fd1.write("      integer :: iErr\n");
   fd1.write("\n");
   fd1.write("      iErr = 0\n");
   return

def define_packages(registry_processed, inc_dir):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   abrev = root.attrib["core_abbrev"]

   """Abre o arquivo define_packages.inc """
   fd1 = open(inc_dir+"/define_packages.inc","w")
   #fd1 = open(inc_dir+"/modDefinePackages.f90","w")
   #fd1.write("module modDefinePackages\n\n")
   #fd1.write("   containss\n\n")
   """Chama a rotina que escreve a primeira parte de define_packages.inc"""
   header_define_packages(fd1,abrev)

   for child in root:
      if child.tag == "packages":
         for gran_child in child:
            fd1.write("      call mpas_pool_add_package(packagePool, '{0}Active', .false.)\n".format(gran_child.attrib["name"]))
         fd1.write("   end function {0}_define_packages\n".format(abrev))
   #fd1.write("end module modDefinePackages\n")
   fd1.close()