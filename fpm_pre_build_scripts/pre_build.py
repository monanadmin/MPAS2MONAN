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
pp_command,version, registry = readToml()
write_log(pp_command)

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
cpp = "cpp -E -I../include/ "+pp_command
fpp = "fypp --include=../setup/core_atmosphere/diagnostics "+pp_command

print("3. Filter xml setup file ..")
filterFypp(monan_base_dir=monan_base_dir,cpp = cpp,fpp = fpp)
monan_base_dir = "../setup/core_init_atmosphere/"
filterFypp(monan_base_dir=monan_base_dir,cpp = cpp,fpp = fpp)

monan_base_dir = "../include"
filterFile(monan_base_dir,"ESMF_Macros.fypp",cpp = cpp,fpp = fpp,new_src=monan_base_dir)
#filterFile(monan_base_dir,"smiol_codes.fypp",cpp = cpp,fpp = fpp,new_src=monan_base_dir)


registry_processed = "../setup/core_atmosphere/Registry_processed.xml"
mod_dir = "../include"

# print("5. Building structs_and_variables.inc ... ")
# struct_and_variables(registry_processed = registry_processed,inc_dir = mod_dir) # <---- Precisa verificar e corrigir!!!!!

# print("6. Building core_variables.inc ... ")
# core_variables_write(registry_processed = registry_processed,inc_dir = mod_dir)

# print("7. Building domain_variables.inc ... ")
# domain_variables(registry_processed = registry_processed,inc_dir = mod_dir)

# print("8. Building define_packages.inc ... ")
# define_packages(registry_processed = registry_processed,inc_dir = mod_dir)

# print("9. Building setup_immutable_streams.inc ... ")
# setup_immutable_streams(registry_processed = registry_processed,inc_dir = mod_dir)

# print("10.Building block_dimension_routines.inc ... ")
# block_dimension_routines(registry_processed = registry_processed,inc_dir = mod_dir)
# pbl.close()

# print("11.Building namelist_call.inc ... ")
# namelist_call(registry_processed = registry_processed,inc_dir = mod_dir)
# pbl.close()

# print("12. Building namelist_defines.inc ... ")
# namelist_defines(registry_processed = registry_processed,inc_dir = mod_dir)
# #sys.exit()

cmd = "cp "+registry+"/*.inc ../include"
returned_value = os.system(cmd)

monan_base_dir = "../include"
for root, dirs, files in os.walk(monan_base_dir):
   for file in files:
      file_name,file_ext  = os.path.splitext(file)
      if file_ext == ".fypp":
         filterFile(monan_base_dir,file,cpp = cpp,fpp = fpp,new_src=monan_base_dir)

monan_base_dir = "../pre_build_src"
cpp = "cpp -E -I../include/ "+pp_command
fpp = "fypp --include=../include "+pp_command
print("13. Filter files with cpp or fypp.for src..")
filterFypp(monan_base_dir=monan_base_dir,cpp = cpp,fpp = fpp)

# print("4. Creating modules directory ... ")
# cmd = "mkdir "+mod_dir
# write_log(cmd)
# returned_value = os.system(cmd)


pbl.close()