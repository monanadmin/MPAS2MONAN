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

def namelistCall(fnc,abrev,fase,nml):
   if fase == 'head':
      fnc.write( "   function {0}_setup_namelists(configPool, namelistFilename, dminfo) result(iErr)\n".format(abrev));
      fnc.write( "      use mpas_derived_types\n");
      fnc.write( "      use mpas_pool_routines\n");
      fnc.write( "      use mpas_io_units\n");
      fnc.write( "      use mpas_abort, only : mpas_dmpar_global_abort\n");
      fnc.write( "      use mpas_log, only : mpas_log_write\n");
      fnc.write( "      implicit none\n");
      fnc.write( "      type (mpas_pool_type), intent(inout) :: configPool\n");
      fnc.write( "      character (len=*), intent(in) :: namelistFilename\n");
      fnc.write( "      type (dm_info), intent(in) :: dminfo\n");
      fnc.write( "      integer :: iErr\n");
      fnc.write( "\n");
      fnc.write( "      integer :: unitNumber\n");
      fnc.write( "      logical :: nmlExists\n");
      fnc.write( "\n");
      fnc.write( "      iErr = 0\n");
      fnc.write( "      unitNumber = 21\n");
      fnc.write( "      call mpas_log_write('Reading namelist from file '//trim(namelistFilename))\n");
      fnc.write( "      inquire(file=trim(namelistFilename), exist=nmlExists)\n");
      fnc.write( "      if ( .not. nmlExists ) then\n");
      fnc.write( "         call mpas_dmpar_global_abort('ERROR: Namelist file '//trim(namelistFilename)//' does not exist.')\n");
      fnc.write( "      end if\n");
      fnc.write( "      open(unitNumber,file=trim(namelistFilename),status='old',form='formatted')\n");
      fnc.write( "\n");
   elif fase == "body":
      fnc.write("      call {0}_setup_nmlrec_{1}(configPool, unitNumber, dminfo)\n".format(abrev, nml))
   elif fase == "tail":
      fnc.write( "\n");
      fnc.write( "      close(unitNumber)\n");
      fnc.write( "   end function {0}_setup_namelists\n".format(abrev));
   return

def namelist_call(registry_processed, inc_dir):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   """Abre o arquivo namelist_call.inc """
   fnc = open(inc_dir+"/namelist_call.inc","w")
   #fnc = open(inc_dir+"/modNamelistCall.f90","w")
   #fnc.write("module modNamelistCall\n\n")
   #fnc.write("   contains\n\n")
   """Faz preenchimento da parte inicial do código em Fortran (header)"""

   abrev = root.attrib["core_abbrev"]
   namelistCall(fnc,abrev,'head','')

   for child in root:
      if child.tag == "nml_record":
         namelistCall(fnc,abrev,'body',child.attrib["name"])

   namelistCall(fnc,abrev,'tail','')

   #fnc.write("end module modNamelistCall\n")
   fnc.close()