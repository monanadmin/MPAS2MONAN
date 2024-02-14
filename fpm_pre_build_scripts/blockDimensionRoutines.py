"""setupImmutableStreams.py
   Description: This python script extracts information for setup_immutable_streams.inc
   to create structs_and_variables.inc.
   inputs:
     core_string - core_stringiation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

import xml.etree.ElementTree as ET
import sys

def block_dimension_routines(registry_processed, inc_dir):

   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   core_string = root.attrib["core_abbrev"]

   #fd = open(inc_dir+"/modBlockDimensionRoutines.f90", "w")
   fd = open(inc_dir+"/block_dimension_routines.inc", "w")   
   #fd.write("module modBlockDimensionRoutines\n\n")
   #fd.write("   contains\n\n")
   fd.write("   function {0}_setup_derived_dimensions(readDimensions, dimensionPool, configPool) result(iErr)\n".format(core_string))
   fd.write("\n")
   fd.write("      use mpas_derived_types\n")
   fd.write("      use mpas_pool_routines\n")
   fd.write("      use mpas_io_units\n")
   fd.write("      use mpas_log, only : mpas_log_write\n")
   fd.write("\n")
   fd.write("      implicit none\n")
   fd.write("\n")
   fd.write("      type (mpas_pool_type), intent(inout) :: readDimensions !< Input: Pool to pull read dimensions from\n")
   fd.write("      type (mpas_pool_type), intent(inout) :: configPool !< Input: Pool containing namelist options with configs\n")
   fd.write("      type (mpas_pool_type), intent(inout) :: dimensionPool !< Input/Output: Pool to add dimensions into\n")
   fd.write("\n")
   fd.write("      integer :: iErr, errLevel\n")
   fd.write("\n")

   for child in root:
      if child.tag == "dims":
         for grand_child in child:
            dimname = grand_child.attrib["name"]
            fd.write("      integer, pointer :: {0}\n".format(dimname))

   for child in root:
      if child.tag == "dims":
         for grand_child in child:
            if grand_child.tag == "dim":
               dimname = grand_child.attrib["name"]
               if "definition" in grand_child.attrib:
                  dimdef = grand_child.attrib["definition"]
                  if dimdef[0:9] == "namelist:":
                     option_name = dimdef[9:]
                     for new_child in root:
                         if new_child.tag == "nml_record":
                           nmlrecname = new_child.attrib["name"]
                           for gg_child in new_child:
                              if gg_child.tag == "nml_option":
                                 nmloptname = gg_child.attrib["name"]
                                 nmlopttype = gg_child.attrib["type"]

                                 if option_name == nmloptname:
                                    if nmlopttype == "real":
                                       fd.write("      real (kind=RKIND), pointer :: {0}\n".format(nmloptname))
                                    elif nmlopttype == "integer":
                                       fd.write("      integer, pointer :: {0}\n".format(nmloptname))
                                    elif nmlopttype == "logical":
                                       fd.write("      logical, pointer :: {0}\n".format(nmloptname))
                                    elif nmlopttype == "character":
                                       fd.write("      character (len=StrKIND), pointer :: {0}\n".format(nmloptname))

   fd.write("\n")
   fd.write("      iErr = 0\n")
   fd.write("      errLevel = mpas_pool_get_error_level()\n")
   fd.write("      call mpas_pool_set_error_level(MPAS_POOL_SILENT)\n")
   fd.write("\n")

   for child in root:
      if child.tag == "dims":
         for grand_child in child:
            if grand_child.tag == "dim":
               dimname = grand_child.attrib["name"]
               if "definition" in grand_child.attrib:
                  dimdef = grand_child.attrib["definition"]
                  if dimdef[0:9] == "namelist:":
                     option_name = dimdef[9:]
                     fd.write("      nullify({0})\n".format(option_name))
                     fd.write("      call mpas_pool_get_config(configPool, '{0}', {0})\n".format(option_name, option_name))

   fd.write("\n")

   for child in root:
      if child.tag == "dims":
         for grand_child in child:
            if grand_child.tag == "dim":
               dimname = grand_child.attrib["name"]
               fd.write("      nullify({0})\n".format(dimname))
               fd.write("      call mpas_pool_get_dimension(dimensionPool, '{0}', {0})\n".format(dimname, dimname))
   fd.write("\n")

   fd.write("      call mpas_log_write('Assigning remaining dimensions from definitions in Registry.xml ...')\n")

   for child in root:
      if child.tag == "dims":
         for grand_child in child:
            if grand_child.tag == "dim":
               dimname = grand_child.attrib["name"]
               if "definition" in grand_child.attrib:
                  fd.write("      call mpas_pool_get_dimension(dimensionPool, '{0}', {0})\n".format(dimname, dimname))
                  fd.write("      if ( .not. associated({0}) ) then\n".format(dimname))
                  fd.write("         allocate({0})\n".format(dimname))
                  dimdef = grand_child.attrib["definition"]
                  if dimdef[0:9] == "namelist:":
                     option_name = dimdef[9:]
                     fd.write("         {0} = {1}\n".format(dimname, option_name))
                     fd.write("         call mpas_log_write('       {0} = $i ({1})', intArgs=(/{1}/))\n".format(dimname, option_name))
                  else:
                     fd.write("         {0} = {1}\n".format(dimname, dimdef))
                     fd.write("         call mpas_log_write('       {0} = $i', intArgs=(/{1}/))\n".format(dimname, dimdef))
                  fd.write("         call mpas_pool_add_dimension(dimensionPool, '{0}', {0})\n".format(dimname, dimname))

                  fd.write("      else if ( {0} == MPAS_MISSING_DIM ) then\n".format(dimname))

                  if dimdef[0:9] == "namelist:":
                     option_name = dimdef[9:]
                     fd.write("         {0} = {1}\n".format(dimname,option_name))
                  else:
                     fd.write("         {0} = {1}\n".format(dimname,dimdef))
                  fd.write("      end if\n\n")
               else:
                  fd.write("      if ( .not. associated({0}) ) then\n".format(dimname))
                  fd.write("         allocate({0})\n".format(dimname))
                  fd.write("         {0} = MPAS_MISSING_DIM\n".format(dimname))
                  fd.write("         call mpas_pool_add_dimension(dimensionPool, '{0}', {0})\n".format(dimname))
                  fd.write("      end if\n\n");

   fd.write("      call mpas_log_write(' ')\n")
   fd.write("      call mpas_log_write(' ----- done assigning dimensions from Registry.xml -----')\n")
   fd.write("      call mpas_log_write(' ')\n")
   fd.write("      call mpas_log_write(' ')\n")
   fd.write("      call mpas_pool_set_error_level(errLevel)\n\n")
   fd.write("   end function {0}_setup_derived_dimensions\n".format(core_string))
   fd.write("\n\n")
   fd.write("   function {0}_setup_decomposed_dimensions(block, manager, readDimensions, dimensionPool, totalBlocks) result(iErr)\n".format(core_string))
   fd.write("\n")
   fd.write("      use mpas_derived_types\n")
   fd.write("      use mpas_decomp\n")
   fd.write("      use mpas_pool_routines\n")
   fd.write("      use mpas_io_units\n")
   fd.write("      use mpas_abort, only : mpas_dmpar_global_abort\n")
   fd.write("      use mpas_log, only : mpas_log_write\n")
   fd.write("\n")
   fd.write("      implicit none\n")
   fd.write("\n")
   fd.write("      type (block_type), intent(inout) :: block !< Input: Pointer to block\n")
   fd.write("      type (mpas_streamManager_type), intent(inout) :: manager !< Input: Stream manager\n")
   fd.write("      type (mpas_pool_type), intent(inout) :: readDimensions !< Input: Pool to pull read dimensions from\n")
   fd.write("      type (mpas_pool_type), intent(inout) :: dimensionPool !< Input/Output: Pool to add dimensions into\n")
   fd.write("      integer, intent(in) :: totalBlocks !< Input: Number of blocks\n")
   fd.write("\n")
   fd.write("      integer :: iErr\n")
   fd.write("      type (field1DInteger), pointer :: ownedIndices\n")
   fd.write("      procedure (mpas_decomp_function), pointer :: decompFunc\n")
   fd.write("\n")

   for child in root:
      if child.tag == "dims":
         for grand_child in child:
            if grand_child.tag == "dim":
               dimname = grand_child.attrib["name"]
               if "decomposition" in grand_child.attrib:
                  dimdecomp = grand_child.attrib["decomposition"]
                  if dimdecomp == "none":
                     fd.write("      integer, pointer :: %{0}}\n".format(dimname))

   fd.write("\n")
   fd.write("      iErr = 0\n")
   fd.write("      call mpas_log_write('Processing decomposed dimensions ...')\n\n")

   for child in root:
      if child.tag == "dims":
         for grand_child in child:
            if grand_child.tag == "dim":
               dimname = grand_child.attrib["name"]
               if "decomposition" in grand_child.attrib:   
                  dimdecomp = grand_child.attrib["decomposition"]
                  if dimdecomp == "none":
                     fd.write("      call mpas_pool_get_dimension(readDimensions, '{0}', {0})\n".format(dimname))
                     fd.write("      if ( .not. associated({0})) then\n".format(dimname))
                     fd.write("         call mpas_log_write('Dimension ''{0}'' was not defined, and cannot be decomposed.', MPAS_LOG_WARN)\n".format(dimname))
                     fd.write("      else\n")
                     fd.write("         call mpas_decomp_get_method(block % domain % decompositions, '{0}', decompFunc, iErr)\n".format(dimdecomp))
                     fd.write("         if ( iErr /= MPAS_DECOMP_NOERR ) then\n")
                     fd.write("            call mpas_dmpar_global_abort('ERROR: Decomposition method \'\'{0}\'\' used by dimension \'\'{1}\'\' does not exist.')\n".format(dimdecomp, dimname))
                     fd.write("         end if\n")
                     fd.write("\n")
                     fd.write("         allocate(ownedIndices)\n")
                     fd.write("         ownedIndices % hasTimeDimension = .false.\n")
                     fd.write("         ownedIndices % isActive = .true.\n")
                     fd.write("         ownedIndices % isVarArray = .false.\n")
                     fd.write("         ownedIndices % isDecomposed = .false.\n")
                     fd.write("         ownedIndices % isPersistent = .true.\n")
                     fd.write("         ownedIndices % defaultValue = 0\n")
                     fd.write("         ownedIndices % fieldName = '{0}OwnedIndices'\n".format(dimname))
                     fd.write("         ownedIndices % dimNames(1) = '{0}'\n".format(dimname))
                     fd.write("         iErr = decompFunc(block, manager, {0}, totalBlocks, ownedIndices % array)\n".format(dimname))
                     fd.write("         ownedIndices % dimSizes(1) = size(ownedIndices % array, dim=1)\n")
                     fd.write("         call mpas_pool_add_field(block % allFields, '{0}OwnedIndices', ownedIndices)\n".format(dimname))
                     fd.write("         call mpas_pool_get_dimension(block % dimensions, '{0}', {0})\n".format(dimname))
                     fd.write("         {0} = size(ownedIndices % array, dim=1)\n".format(dimname))
                     fd.write("         call mpas_log_write('       {0} => $i indices owned by block $i', intArgs=(/{0}, block % blockID/))\n".format(dimname))
                     fd.write("      end if\n")

   fd.write("      call mpas_log_write(' ')\n")
   fd.write("      call mpas_log_write(' ----- done processing decomposed dimensions -----')\n")
   fd.write("      call mpas_log_write(' ')\n")
   fd.write("      call mpas_log_write(' ')\n")
   fd.write("\n")
   fd.write("   end function {0}_setup_decomposed_dimensions\n".format(core_string))
   #fd.write("end module modBlockDimensionRoutines\n")
   fd.close()