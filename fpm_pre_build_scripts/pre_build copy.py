import sys
import os

from filterFypp import filterFypp
from readToml import readToml
from createToml4FPM import createToml4FPM
# To namlists, includes and streams
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

print("\n\n\n#     # ####### #     #    #    #     #")
print("##   ## #     # ##    #   # #   ##    #")
print("# # # # #     # # #   #  #   #  # #   #")
print("#  #  # #     # #  #  # #     # #  #  #")
print("#     # #     # #   # # ####### #   # #")
print("#     # #     # #    ## #     # #    ##")
print("#     # ####### #     # #     # #     #\n\n")
print("--------- The pre build system -------\n\n")


tomlFile = sys.argv[1]
monan_base_dir = sys.argv[2]
registry = sys.argv[3]

#Directory to put namelists and streams
namelist_dir = monan_base_dir+"/namelists"
#Directory to put registry.xml dependent modules (old includes)
inc_dir = monan_base_dir+"/src/inc"

createToml4FPM(atm_dir="./",version="0.1.0")
sys.exit()

if not os.path.exists(namelist_dir):
   os.mkdir(namelist_dir)

if not os.path.exists(inc_dir):
   os.mkdir(inc_dir)

#Copy registry to base_src
cmd = "cp {0} {1}".format(registry,monan_base_dir+"/base_src/")
returned_value = os.system(cmd)

#Get the directives (-D) from tomlFile and put in command to filter sources .F90 into .f90
# The tomlFile contains the information that is needed to create the bin of MONAN
cpp_command,version = readToml(tomlFile=tomlFile)

#Apply the FYPP filter in each file using cmd_prefix F90 -> f90
filterFypp(monan_base_dir=monan_base_dir,cmd_prefix=cpp_command)

registry_processed = monan_base_dir+"/src/Registry_processed.xml"

#Create the FPM TOML base file
createToml4FPM(atm_dir=monan_base_dir,version=version)

#Moving the main program to app dir (fpm rules)
cmd = "mv {0} {1}".format(monan_base_dir+"/src/driver/mpas.f90",monan_base_dir+"/app/main.f90")
returned_value = os.system(cmd)

# print("01. Doing namelist_write ...")
# namelist_write(registry_processed)

print("\n\nBuilding modNamelistCall.f90 ...")
namelist_call(registry_processed = registry_processed,inc_dir = inc_dir)

print("Building modNamelistDefines.f90 ... ")
namelist_defines(registry_processed = registry_processed,inc_dir = inc_dir)

# print("04. Writing all streams ...")
# streams_write(registry_processed)

print("Building modConfigGet.f90 ... ")
config_get(registry_processed = registry_processed,inc_dir = inc_dir)

print("Building modConfigDeclare.f90 ... ")
config_declare(registry_processed = registry_processed,inc_dir = inc_dir)

print("Building modStructsAndVariables.f90 ... ")
struct_and_variables(registry_processed = registry_processed,inc_dir = inc_dir) # <---- Precisa verificar e corrigir!!!!!

print("Building modCoreVariables.f90 ... ")
core_variables_write(registry_processed = registry_processed,inc_dir = inc_dir)

print("Building modDomainVariables.f90 ... ")
domain_variables(registry_processed = registry_processed,inc_dir = inc_dir)

print("Building modDefinePackages.f90 ... ")
define_packages(registry_processed = registry_processed,inc_dir = inc_dir)

print("Building modSetupImmutableStreams.f90 ... ")
setup_immutable_streams(registry_processed = registry_processed,inc_dir = inc_dir)

print("Building modBlockDimensionRoutines.f90 ... ")
block_dimension_routines(registry_processed = registry_processed,inc_dir = inc_dir)

print("\n\n\nAll done!")
print("\n\n\n")