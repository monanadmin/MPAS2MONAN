import sys
import os
from datetime import datetime
from readToml import readToml
from filterFypp import filterFypp,filterFile
from structsAndVariables import struct_and_variables
from domainsVariables import domain_variables
from coreVariables import core_variables_write
from allStreams import streams_write
from configDeclare import config_declare
from configGet import config_get
from namelistCall import namelist_call
from definePackages import define_packages
from namelistDefines import namelist_defines
from namelist import namelist_write
from setupImmutableStreams import setup_immutable_streams
from blockDimensionRoutines import block_dimension_routines

def write_log(message):
   now = datetime.now()
   dt_string = now.strftime("%Y%m%d%H%M%S")
   pbl.write("{0} {1}\n".format(dt_string,message))

#Open a log file to write the steps
pbl = open("pre_build.log","w")
write_log("Initial time of pre-build")

#Read the "../setup/monan_setup.toml" to setup the model
print("1. Reading the setup to pre_build...")
pp_command,version,registry,netcdf_dir,hdf5_dir,pnetcdf_dir,mpi_dir,pio_dir = readToml()
write_log(pp_command)

all_includes = [netcdf_dir,hdf5_dir,pnetcdf_dir,mpi_dir,pio_dir]


print("2. Creating the src directory to receive the sources .f90...")
cmd = "cp -R ../pre_build_src ../src"
returned_value = os.system(cmd)
write_log("src created")

#Clean the src directory from files
for root, dirs, files in os.walk("../src"):
   for file in files:
      cmd = "rm {0}/{1}".format(root,file)
      write_log(cmd)
      returned_value = os.system(cmd)

monan_base_dir = "../setup/core_atmosphere/"
include = "-I../include/"
for i in all_includes:
   include = include + " -I"+i+"/include"
cpp = "cpp -E "+include+" "+pp_command
include = " -I../setup/core_atmosphere/diagnostics"
for i in all_includes:
   include = include + " -I"+i+"/include"
fpp = "fypp "+include+" "+pp_command

print("3. Filter xml setup file ..")
filterFypp(monan_base_dir=monan_base_dir,cpp = cpp,fpp = fpp)
monan_base_dir = "../setup/core_init_atmosphere/"
filterFypp(monan_base_dir=monan_base_dir,cpp = cpp,fpp = fpp)

print("4. Filter ESMF_Macros.fypp ..")
monan_base_dir = "../include"
filterFile(monan_base_dir,"ESMF_Macros.fypp",cpp = cpp,fpp = fpp,new_src=monan_base_dir)
#filterFile(monan_base_dir,"smiol_codes.fypp",cpp = cpp,fpp = fpp,new_src=monan_base_dir)

print("5. Generating the includes from registry ..")
registry_processed = "../setup/core_atmosphere/Registry_processed.xml"
mod_dir = "../include"
registry_exe = registry+"/bin/registry"
registry_processed = "../setup/core_atmosphere/Registry_processed.xml"
cmd = registry_exe+" "+registry_processed
returned_value = os.system(cmd)

print("6. Copy the includes from registry ..")
cmd = "cp ./*.inc ../include"
returned_value = os.system(cmd)

include = "-I../include/"
for i in all_includes:
   include = include + " -I"+i+"/include"
cpp = "cpp -E "+include+" "+pp_command
include = " -I../include/"
for i in all_includes:
   include = include + " -I"+i+"/include"
fpp = "fypp "+include+" "+pp_command
print("7. Filter include dir ..")
monan_base_dir = "../include"
for root, dirs, files in os.walk(monan_base_dir):
   for file in files:
      file_name,file_ext  = os.path.splitext(file)
      if file_ext == ".fypp":
         filterFile(monan_base_dir,file,cpp = cpp,fpp = fpp,new_src=monan_base_dir)

include = "-I../include/"
for i in all_includes:
   include = include + " -I"+i+"/include"
cpp = "cpp -E "+include+" "+pp_command
include = " -I../include/"
for i in all_includes:
   include = include + " -I"+i+"/include"
fpp = "fypp "+include+" "+pp_command
monan_base_dir = "../pre_build_src"
print("8. Filter pre_build_src ..")
filterFypp(monan_base_dir=monan_base_dir,cpp = cpp,fpp = fpp)
#cpp = "cpp -E -I../include/ "+pp_command
#fpp = "fypp --include=../include "+pp_command

pbl.close()