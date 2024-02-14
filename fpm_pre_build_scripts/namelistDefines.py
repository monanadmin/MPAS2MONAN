"""namelistDefines.py
   Description: This python script namelist_defines.inc
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys


def fillDefines(fd,varsDict,section):
   """Preenche as 3 outras partes do namelist_defines.inc"""
   fd.write("\n\n      namelist /{0}/ &\n".format(section))
   itens = varsDict.keys()
   size = len(itens)
   cnt = 0
   for item in itens:
      cnt = cnt+1
      if cnt < size:
         fd.write("         {0}, &\n".format(item))
      else:
         fd.write("         {0} \n".format(item))
   fd.write("      if (dminfo % my_proc_id == IO_NODE) then\n")
   fd.write("! Rewinding before each read leads to errors when the code is built with\n")
   fd.write("! the NAG Fortran compiler. If building with NAG, be kind and don't rewind.\n")
   fd.write('#:if not defined("NAG_COMPILER")\n')
   fd.write("         rewind(unitNumber)\n")
   fd.write("#:endif\n")
   fd.write("         read(unitNumber, {0}, iostat=ierr)\n".format(section))
   fd.write("      end if\n")
   fd.write("      call mpas_dmpar_bcast_int(dminfo, ierr)\n\n")
   fd.write("      if (ierr <= 0) then\n")

   itens = varsDict.keys()
   for item in itens:
      if varsDict[item] == "character":
         fd.write("         call mpas_dmpar_bcast_char(dminfo, {0})\n".format(item))
      elif varsDict[item] == "integer":
         fd.write("         call mpas_dmpar_bcast_int(dminfo, {0})\n".format(item))
      else:
         fd.write("         call mpas_dmpar_bcast_{0}(dminfo, {1})\n".format(varsDict[item],item))
   fd.write("         if (ierr < 0) then\n")
   fd.write("            call mpas_log_write('*** Encountered an issue while attempting to read namelist record {0}')\n".format(section))
   fd.write("            call mpas_log_write('    The following values will be used for variables in this record:')\n")
   fd.write("            call mpas_log_write(' ')\n")
   for item in itens:
      if varsDict[item] == "character":
         fd.write("            call mpas_log_write('        {0} = '//mpas_log_escape_dollars({0}))\n".format(item))
      elif varsDict[item] == "integer":
         fd.write("            call mpas_log_write('        {0} = $i', intArgs=(/{0}/))\n".format(item))
      elif varsDict[item] == "real":
         fd.write("            call mpas_log_write('        {0} = $r', realArgs=(/{0}/))\n".format(item))
      elif varsDict[item] == "logical":
         fd.write("            call mpas_log_write('        {0} = $l', logicArgs=(/{0}/))\n".format(item))
   fd.write("            call mpas_log_write(' ')\n")
   fd.write("         end if\n")
   fd.write("      else if (ierr > 0) then\n")
   fd.write("         call mpas_log_write('Error while reading namelist record nhyd_model.', MPAS_LOG_CRIT)\n")
   fd.write("      end if\n\n")

   for item in itens:
      fd.write("      call mpas_pool_add_config(configPool, '{0}', {0})\n".format(item))

   fd.write("   end subroutine atm_setup_nmlrec_{0}\n\n".format(section))

   return

def fillVarsInNamelist_defines(fd,gran_child,varsDict):
   """O trecho abaixo preenche o namelist_defines.inc com as variáveis do namelist - Primeira parte do arquivo"""
   if gran_child.attrib["type"] == "real":
      fd.write("      real (kind=RKIND) :: {0} = {1}\n".format(gran_child.attrib["name"], gran_child.attrib["default_value"]));
   elif gran_child.attrib["type"] == "integer":
      fd.write("      integer :: {0} = {1}\n".format(gran_child.attrib["name"], gran_child.attrib["default_value"]));
   elif gran_child.attrib["type"] == "logical":
      if gran_child.attrib["default_value"] == "true":
         fd.write("      logical :: {0} = {1}\n".format(gran_child.attrib["name"], ".true."));
      else:
         fd.write("      logical :: {0} = {1}\n".format(gran_child.attrib["name"], ".false."));
   elif gran_child.attrib["type"] == "character":
      fd.write("      character (len=StrKIND) :: {0} = '{1}'\n".format(gran_child.attrib["name"], gran_child.attrib["default_value"]));
   
   """Coloca a variável lida e seu tipo num dicionário para ser usado nas demais partes do namelist_defines.inc"""
   varsDict[gran_child.attrib["name"]]=gran_child.attrib["type"]

   return varsDict

def namelist_defines(registry_processed,inc_dir):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   abrev = root.attrib["core_abbrev"]
   
   """Abre o arquivo namelist_defines.inc """
   fd = open(inc_dir+"/namelist_defines.inc","w")
   #fd = open(inc_dir+"/modNamelistDefines.f90","w")   
   #fd.write("module modNamelistDefines\n\n")
   #fd.write("   contains\n\n")
   for child in root:
      if child.tag == "nml_record":
         varsDict={}
         
         """Start defining new subroutine for namelist record. writing in namelist_defines.inc"""
         fd.write("   subroutine {0}_setup_nmlrec_{1}(configPool, unitNumber, dminfo)\n".format(abrev, child.attrib["name"]));
         fd.write("      use mpas_log, only : mpas_log_write, mpas_log_escape_dollars\n");
         fd.write("      implicit none\n");
         fd.write("      type (mpas_pool_type), intent(inout) :: configPool\n");
         fd.write("      integer, intent(in) :: unitNumber\n");
         fd.write("      type (dm_info), intent(in) :: dminfo\n");
         fd.write("      type (mpas_pool_type), pointer :: recordPool\n");
         fd.write("      integer :: ierr\n");
         fd.write("\n");
         for gran_child in child:
            if gran_child.tag == "nml_option":
               """preenche o namelist_defines.inc com as variáveis - primeira parte"""
               fillVarsInNamelist_defines(fd,gran_child,varsDict)
      
         fillDefines(fd,varsDict, child.attrib["name"])
   #fd.write("end module modNamelistDefines\n")
   fd.close()