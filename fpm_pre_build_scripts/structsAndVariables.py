"""structs_and_variables.py
   Description: This python script receives and extracts information
   to create structs_and_variables.inc.
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

import xml.etree.ElementTree as ET
import sys

def writeIntermInfo(fsav):
   fsav.write("\n")
   fsav.write("\n")
   fsav.write("      integer :: numConstituents\n")
   fsav.write("\n")
   fsav.write("      nullify(newSubPool)\n")
   fsav.write("      group_counter = -1\n")
   fsav.write("      group_started = .false.\n")
   fsav.write("      group_start = -1\n")
   return

def write_field_pointer_arrays(fsav):
   fsav.write("\n");
   fsav.write("      type (field0DReal), pointer :: r0Ptr\n");
   fsav.write("      type (field1DReal), pointer :: r1Ptr\n");
   fsav.write("      type (field2DReal), pointer :: r2Ptr\n");
   fsav.write("      type (field3DReal), pointer :: r3Ptr\n");
   fsav.write("      type (field4DReal), pointer :: r4Ptr\n");
   fsav.write("      type (field5DReal), pointer :: r5Ptr\n");
   fsav.write("      type (field0DInteger), pointer :: i0Ptr\n");
   fsav.write("      type (field1DInteger), pointer :: i1Ptr\n");
   fsav.write("      type (field2DInteger), pointer :: i2Ptr\n");
   fsav.write("      type (field3DInteger), pointer :: i3Ptr\n");
   fsav.write("      type (field0DChar), pointer :: c0Ptr\n");
   fsav.write("      type (field1DChar), pointer :: c1Ptr\n");
   fsav.write("      type (field0DReal), dimension(:), pointer :: r0aPtr\n");
   fsav.write("      type (field1DReal), dimension(:), pointer :: r1aPtr\n");
   fsav.write("      type (field2DReal), dimension(:), pointer :: r2aPtr\n");
   fsav.write("      type (field3DReal), dimension(:), pointer :: r3aPtr\n");
   fsav.write("      type (field4DReal), dimension(:), pointer :: r4aPtr\n");
   fsav.write("      type (field5DReal), dimension(:), pointer :: r5aPtr\n");
   fsav.write("      type (field0DInteger), dimension(:), pointer :: i0aPtr\n");
   fsav.write("      type (field1DInteger), dimension(:), pointer :: i1aPtr\n");
   fsav.write("      type (field2DInteger), dimension(:), pointer :: i2aPtr\n");
   fsav.write("      type (field3DInteger), dimension(:), pointer :: i3aPtr\n");
   fsav.write("      type (field0DChar), dimension(:), pointer :: c0aPtr\n");
   fsav.write("      type (field1DChar), dimension(:), pointer :: c1aPtr\n");
   fsav.write("\n");
   fsav.write("      type (mpas_pool_type), pointer :: newSubPool\n");
   fsav.write("      integer :: group_counter\n");
   fsav.write("      logical :: group_started\n");
   fsav.write("      integer :: group_start\n");
   fsav.write("      integer :: index_counter\n");
   fsav.write("      integer, pointer :: const_index\n");
   fsav.write("\n");
   return

def struct_and_variables(registry_processed, inc_dir):

   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   abrev = root.attrib["core_abbrev"]

   """Abre o arquivo structs_and_variables.inc """
   #fsav = open(inc_dir+"/modStructsAndVariables.f90", "w")
   fsav = open(inc_dir+"/structs_and_variables.inc", "w")

   #fsav.write("module modStructsAndVariables\n\n")
   #fsav.write("   contains\n\n")

   for child in root:
      if child.tag == "var_struct":
         structname = child.attrib["name"]
         if "name_in_code" in child.attrib:
            structnameincode = child.attrib["name_in_code"]
         else:
            structnameincode = structname
         fsav.write("   subroutine {0}_generate_{1}_{2}(block, structPool, dimensionPool, packagePool)\n".format(abrev,"pool",structname))
         fsav.write("      use mpas_derived_types\n")
         fsav.write("      use mpas_io_units\n")
         fsav.write("      implicit none\n")
         fsav.write("      type (block_type), pointer, intent(inout) :: block\n")
         fsav.write("      type (mpas_pool_type), intent(inout) :: structPool\n")
         fsav.write("      type (mpas_pool_type), intent(inout) :: dimensionPool\n")
         fsav.write("      type (mpas_pool_type), intent(in) :: packagePool\n")

         write_field_pointer_arrays(fsav)
         for child in root:
            """Se for packages preencher o define_packages.inc"""
            if child.tag == "packages":
               for gran_child in child:
                  fsav.write("      logical, pointer :: {0}Active\n".format(gran_child.attrib["name"]))
         writeIntermInfo(fsav)
         for child in root:
            if child.tag == "packages":
               for gran_child in child:
                  fsav.write("      call mpas_pool_get_package(packagePool, '{0}Active', {0}Active)\n".format(gran_child.attrib["name"]))
         fsav.write("\n")
         fsav.write("      allocate(newSubPool)\n")
         fsav.write("      call mpas_pool_create_pool(newSubPool)\n")
         fsav.write("      call mpas_pool_add_subpool(structPool, '{0}', newSubPool)\n".format(structnameincode))
         fsav.write("      call mpas_pool_add_subpool(block % allStructs, '{0}', newSubPool)\n".format(structname))
         fsav.write("\n")
#         for child in root:
#            if child.tag == "var_array":
         fsav.write("   end subroutine {0}_generate_{1}_{2}\n".format(abrev,"pool",structname))
   #fsav.write("\n\nend module modStructsAndVariables\n")       

   fsav.close()
   return


