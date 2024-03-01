"""registry.py
   Description: This python script generate a lot of includes for fortran routines
   accordingly the Registry_processed.xml

        USAGE: python registry.py <registry_processed> <output_dir>
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2024, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys
import os
import subprocess
from readToml import readToml

REAL = 1
INTEGER = 2
CHARACTER = 3


def get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def write_model_variables(registry,output_dir):
   modelname = registry.attrib["model"]
   corename = registry.attrib["core"]
   version = registry.attrib["version"]
   git_ver = get_git_revision_hash()

   pp_command,version,registry,netcdf_dir,hdf5_dir,pnetcdf_dir,mpi_dir,pio_dir,fpm_command,build_target,exe_name = readToml("../base_files/defines.toml")

   fd = open(output_dir+"/"+"core_variables.inc","w")
   fd.write("       core %% modelName = '{0}'\n"     .format(modelname))
   fd.write("       core %% coreName = '{0}'\n"      .format(corename))
   fd.write("       core %% modelVersion = '{0}'\n"  .format(version))
   fd.write("       core %% executableName = '{0}'\n".format(exe_name))
   fd.write("       core %% git_version = '{0}'\n"   .format(git_ver))
   fd.write("       core %% build_target = '{0}'\n"  .format(build_target))
   fd.close()

   fd = open(output_dir+"/"+"domain_variables.inc", "w");
   fd.write("       domain %% namelist_filename = 'namelist.{0}'\n".format(corename))
   fd.write("       domain %% streams_filename = 'streams.{0}'\n"  .format(corename))
   fd.close()

   return

def write_field_pointer_arrays():
   fd.write("\n")
   fd.write("      type (field0DReal), pointer :: r0Ptr\n")
   fd.write("      type (field1DReal), pointer :: r1Ptr\n")
   fd.write("      type (field2DReal), pointer :: r2Ptr\n")
   fd.write("      type (field3DReal), pointer :: r3Ptr\n")
   fd.write("      type (field4DReal), pointer :: r4Ptr\n")
   fd.write("      type (field5DReal), pointer :: r5Ptr\n")
   fd.write("      type (field0DInteger), pointer :: i0Ptr\n")
   fd.write("      type (field1DInteger), pointer :: i1Ptr\n")
   fd.write("      type (field2DInteger), pointer :: i2Ptr\n")
   fd.write("      type (field3DInteger), pointer :: i3Ptr\n")
   fd.write("      type (field0DChar), pointer :: c0Ptr\n")
   fd.write("      type (field1DChar), pointer :: c1Ptr\n")
   fd.write("      type (field0DReal), dimension(:), pointer :: r0aPtr\n")
   fd.write("      type (field1DReal), dimension(:), pointer :: r1aPtr\n")
   fd.write("      type (field2DReal), dimension(:), pointer :: r2aPtr\n")
   fd.write("      type (field3DReal), dimension(:), pointer :: r3aPtr\n")
   fd.write("      type (field4DReal), dimension(:), pointer :: r4aPtr\n")
   fd.write("      type (field5DReal), dimension(:), pointer :: r5aPtr\n")
   fd.write("      type (field0DInteger), dimension(:), pointer :: i0aPtr\n")
   fd.write("      type (field1DInteger), dimension(:), pointer :: i1aPtr\n")
   fd.write("      type (field2DInteger), dimension(:), pointer :: i2aPtr\n")
   fd.write("      type (field3DInteger), dimension(:), pointer :: i3aPtr\n")
   fd.write("      type (field0DChar), dimension(:), pointer :: c0aPtr\n")
   fd.write("      type (field1DChar), dimension(:), pointer :: c1aPtr\n")
   fd.write("\n")
   return

def set_pointer_name(type,ndims,pointer_name,time_levs):
   if time_levs > 1:
      suffix="aPtr"
   else:
      suffix="Ptr"

   if type == REAL:
      pointer_name = "r{0}{1}".format(ndims,suffix)
   elif type == INTEGER:
      pointer_name = "i{0}{1}".format(ndims,suffix)
   elif type == CHARACTER:
      pointer_name = "c{0}{1}".format(ndims,suffix)
   return

def parse_packages_from_registry(registry,output_dir):
   fd = open(output_dir+"/"+"define_packages.inc", "w")
   const_core = registry.attrib["core_abbrev"]
   fd.write("   function {0}_define_packages(packagePool) result(iErr)\n".format(const_core))
   fd.write("      use mpas_derived_types\n")
   fd.write("      use mpas_pool_routines\n")
   fd.write("      use mpas_io_units\n")
   fd.write("      implicit none\n")
   fd.write("      type (mpas_pool_type), intent(inout) :: packagePool !< Input: MPAS Pool for containing package logicals.\n\n")
   fd.write("      integer :: iErr\n")
   fd.write("\n")
   fd.write("      iErr = 0\n")
   for child in registry:
      if child.tag == "packages":
         for grand_child in child:
            if grand_child.tag == "package":
               packagename = grand_child.attrib["name"]
               packagedesc = grand_child.attrib["description"]
               fd.write("      call mpas_pool_add_package(packagePool, '{0}Active', .false.)\n".format(packagename))
   fd.write("   end function {0}_define_packages\n".format(const_core))
   fd.close()




registry_file = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.isdir(output_dir):
   try:
      cmd = "mkdir "+output_dir
      returned_value = os.system(cmd)
   except:
      print("Could not create the dir "+output_dir)
      print("please check!")
      sys.exit()

"""Read xml and put in a structured tree"""
try:
   tree = ET.parse(registry_file)
except:
   print("Error: I can't parse file ",registry_file)
   print("Check if file exist!")
   sys.exit()
registry = tree.getroot()

write_model_variables(registry,output_dir )
parse_packages_from_registry(registry,output_dir)
