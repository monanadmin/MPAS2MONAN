"""setupImmutableStreams.py
   Description: This python script extracts information for setup_immutable_streams.inc
   to create structs_and_variables.inc.
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

import xml.etree.ElementTree as ET
import sys

def setup_immutable_streams(registry_processed, inc_dir):

   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(registry_processed)
   root = tree.getroot()

   abrev = root.attrib["core_abbrev"]

   fd = open(inc_dir+"/setup_immutable_streams.inc", "w")
   #fd.write("module modSetupImmutableStreams\n\n")

   #fd.write("   contains\n\n")

   fd.write("function {0}_setup_immutable_streams(manager) result(iErr)\n\n".format(abrev))
   fd.write("   use MPAS_derived_types, only : MPAS_streamManager_type, &\n")
   fd.write("                                  MPAS_STREAM_INPUT_OUTPUT, MPAS_STREAM_INPUT, &\n")
   fd.write("                                  MPAS_STREAM_OUTPUT, MPAS_STREAM_NONE, MPAS_STREAM_PROPERTY_IMMUTABLE\n")
   fd.write("   use MPAS_stream_manager, only : MPAS_stream_mgr_create_stream, MPAS_stream_mgr_set_property, &\n")
   fd.write("                                   MPAS_stream_mgr_add_field, MPAS_stream_mgr_add_pool\n")
   fd.write("   use mpas_io_units\n\n")
   fd.write("   implicit none\n\n")
   fd.write("   type (MPAS_streamManager_type), pointer :: manager\n")
   fd.write("   character (len=StrKIND) :: packages\n")
   fd.write("   integer :: iErr\n\n")
   fd.write("   iErr = 0\n\n")

   for child in root:
      if child.tag == "streams":
         for grand_child in child:
            if grand_child.tag == "stream":
               optimmutable = "false"
               if "immutable" in grand_child.attrib:
                  optimmutable = grand_child.attrib["immutable"]
               if optimmutable == "true":
                  optname = grand_child.attrib["name"]
                  opttype = grand_child.attrib["type"]
                  optfilename = grand_child.attrib["filename_template"]
                  if opttype == "input;output":
                     fd.write("   call MPAS_stream_mgr_create_stream(manager, \'{0}\', MPAS_STREAM_INPUT_OUTPUT, \'{1}\', ierr=ierr)\n".format(optname, optfilename))
                  elif opttype == "input":
                     fd.write("   call MPAS_stream_mgr_create_stream(manager, \'{0}\', MPAS_STREAM_INPUT, \'{1}\', ierr=ierr)\n".format(optname, optfilename))
                  elif opttype == "output":
                     fd.write("   call MPAS_stream_mgr_create_stream(manager, \'{0}\', MPAS_STREAM_OUTPUT, \'{1}\', ierr=ierr)\n".format(optname, optfilename))
                  else:
                     fd.write("   call MPAS_stream_mgr_create_stream(manager, \'{0}\', MPAS_STREAM_NONE, \'{1}\', ierr=ierr)\n".format(optname, optfilename))
               
                  isPackages = False


                  for gg_child in grand_child:
                     if gg_child.tag == "var":
                        optvarname = gg_child.attrib["name"]
                        isPackages = False
                        if "packages" in gg_child.attrib:
                           optpackages = gg_child.attrib["packages"]
                           isPackages = True
                           fd.write("   write(packages,\'(a)\') \'{0}\'\n".format(optpackages))
                        if isPackages:
                           fd.write("   call MPAS_stream_mgr_add_field(manager, \'{0}\', \'{1}\', packages=packages, ierr=ierr)\n".format(optname, optvarname))
                        else:
                           fd.write("   call MPAS_stream_mgr_add_field(manager, \'{0}\', \'{1}\', ierr=ierr)\n".format(optname, optvarname))
                     if gg_child.tag == "var_array":
                        optvarname = gg_child.attrib["name"]
                        isPackages = False
                        if "packages" in gg_child.attrib:
                           optpackages = gg_child.attrib["packages"]
                           isPackages = True
                           fd.write("   write(packages,\'(a)\') \'{0}\'\n".format(optpackages))
                        if isPackages:
                           fd.write("   call MPAS_stream_mgr_add_field(manager, \'{0}\', \'{1}\', packages=packages, ierr=ierr)\n".format(optname, optvarname))
                        else:
                           fd.write("   call MPAS_stream_mgr_add_field(manager, \'{0}\', \'{1}\', ierr=ierr)\n".format(optname, optvarname))
                     if gg_child.tag == "var_struct":
                        optvarname = gg_child.attrib["name"]
                        isPackages = False
                        if "packages" in gg_child.attrib:
                           optpackages = gg_child.attrib["packages"]
                           isPackages = True
                           fd.write("   write(packages,\'(a)\') \'{0}\'\n".format(optpackages))
                        if isPackages:
                           fd.write("   call MPAS_stream_mgr_add_pool(manager, \'{0}\', \'{1}\', packages=packages, ierr=ierr)\n".format(optname, optvarname))
                        else:
                           fd.write("   call MPAS_stream_mgr_add_pool(manager, \'{0}\', \'{1}\', ierr=ierr)\n".format(optname, optvarname))

                  fd.write("   call MPAS_stream_mgr_set_property(manager, \'{0}\', MPAS_STREAM_PROPERTY_IMMUTABLE, .true., ierr=ierr)\n\n".format(optname))
   fd.write("end function {0}_setup_immutable_streams\n".format(abrev))
   #fd.write("end module modSetupImmutableStreams\n")
   fd.close()