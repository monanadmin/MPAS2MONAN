import sys
import os
from datetime import datetime
from changeDefines import changeDefines
import requests

'''
mpas2monan is a script to copy MPAS structure to a MONAN structure

Author: Rodrigues, L.F. [LFR]
email: luiz.rodrigues@inpe.br
Date: 2024Jan30
rev: 0.1.0

inputs: the original MPAS directory
outputs: the new MONAN directory

How to use: python mpas2monan <input MPAS dir> <output MONAN dir>

Dependencies: 

* fpm installed -See: https://github.com/fortran-lang/fpm/releases
* fypp installed - See: https://github.com/aradi/fypp

'''

def write_log(message):
   now = datetime.now()
   dt_string = now.strftime("%Y%m%d%H%M%S")
   pbl.write("{0} {1}\n".format(dt_string,message))


command = sys.argv[0]
monan_setup = command[0:-21]+"base_files/defines.toml"
monan_fpm = command[0:-21]+"base_files/fpm.toml"
monan_modified = command[0:-21]+"modified_fonts/"
monan_scripts = command[0:-21]+"fpm_pre_build_scripts/"
monan_readme = command[0:-21]+"base_files/README.md"

mpas_dir = sys.argv[1]
monan_dir = os.getcwd()
print("\n\n\n#     # ####### #     #    #    #     #")
print("##   ## #     # ##    #   # #   ##    #")
print("# # # # #     # # #   #  #   #  # #   #")
print("#  #  # #     # #  #  # #     # #  #  #")
print("#     # #     # #   # # ####### #   # #")
print("#     # #     # #    ## #     # #    ##")
print("#     # ####### #     # #     # #     #\n\n")
print("-- The copy MPAS - MONAN system -------\n\n")

#Open a log file to write the steps
pbl = open("mpas2monan.log","w")
write_log("Initial time of conversion")


print("Monan new dir will be ",monan_dir+"/monan")
if os.path.exists(monan_dir+"/monan"):
   print("The directory monan exist!")
   now = datetime.now()
   dt_string = now.strftime("%Y%m%d%H%M%S")
   print("it will be moved to monan."+dt_string+" directory")
   write_log("Path already exists...will be moved to monan."+dt_string)
   cmd = "mv {0} {1}".format(monan_dir+"/monan",monan_dir+"/monan."+dt_string)
   returned_value = os.system(cmd)

'''
The fpm new command creates a new structure to a MONAN dir
'''
print("1. Creating monan FPM structure...")
cmd = "fpm new monan --backfill"
try:
   returned_value = os.system(cmd)
   write_log("New fpm structure created")
except:
   print("Error when making fpm new!")
   print("Check if fpm command is installed and try again!")
   write_log("Error when try to create FPM strucuture")
   sys.exit()

print("2. Cleaning test sources made by fpm...")
'''Clean the src and app directory created by fpm. Preserve the structure'''
for root, dirs, files in os.walk("./monan/src"):
   for file in files:
      cmd = "rm {0}/{1}".format(root,file)
      write_log(cmd)
      returned_value = os.system(cmd)
for root, dirs, files in os.walk("./monan/app"):
   for file in files:
      cmd = "rm {0}/{1}".format(root,file)
      write_log(cmd)
      returned_value = os.system(cmd)

print("3. Creating the include directory used by monan...")
'''Create a necessary include directory'''
cmd = "mkdir ./monan/include"
write_log(cmd)
returned_value = os.system(cmd)

print("4. Creating the setup directory structure used by monan...")
'''Create a necessary setup directory'''
cmd = "mkdir ./monan/setup"
write_log(cmd)
returned_value = os.system(cmd)
cmd = "mkdir ./monan/setup/core_atmosphere"
write_log(cmd)
returned_value = os.system(cmd)
cmd = "mkdir ./monan/setup/core_atmosphere/diagnostics"
write_log(cmd)
returned_value = os.system(cmd)
cmd = "mkdir ./monan/setup/core_init_atmosphere"
write_log(cmd)
returned_value = os.system(cmd)

print("5. Creating the scripts directory used by monan...")
'''Create a necessary scripts directory'''
cmd = "mkdir ./monan/scripts"
write_log(cmd)
returned_value = os.system(cmd)

#print("5. created the src substructure to monan...")
#'''Create the strucuture os subdirectoris in monan/src. All the atm_struct will be created
#'''
atm_struct = ["/src/core_atmosphere","/src/driver","/src/framework","/src/operators","/src/core_init_atmosphere"]
#for dirm in atm_struct:
#   cmd = "mkdir ./monan"+dirm
#   returned_value = os.system(cmd)

print("6. Copy all sources files from MPAS to monan...")
'''Copy all sources files from MPAS to monan:
The files to be copy are "c", "F","inc","xml","h",
'''
for dirm in atm_struct:
   for root, dirs, files in os.walk(mpas_dir+dirm):

      #Get the size of mpas_dir to cut in root
      beg = len(mpas_dir)
      #create the base name to monan by dir of monan plus root cutted from beg
      base = "./monan"+root[beg:]
      #If the dir do not exist will be created
      if not os.path.exists(base):
         print("6.1 Creating sub-dir ",base)
         cmd = "mkdir "+base
         write_log(cmd)
         returned_value = os.system(cmd)
      #Run over all files and make a copy if necessary
      # .inc and .h will be copy in monan/include
      # .xml in monan/setup
      # .F or .c in same directory than MPAS
      for file in files:
         if os.path.islink(root+"/"+file):
            continue
         if file.endswith(".F") or file.endswith(".c") or file.endswith(".inc") or file.endswith(".xml") or file.endswith(".h") or file.endswith(".f90") or file.endswith(".F90"):
            print("6.2 Copy the ",file.strip()," from ",root)
            if file.endswith(".inc") or file.endswith(".h"):
               cmd = "cp "+root.strip()+"/"+file+" "+"./monan/include/"+file
               write_log(cmd)
               returned_value = os.system(cmd)
            else:
               cmd = "cp "+root.strip()+"/"+file+" "+base+"/"+file
               write_log(cmd)
               returned_value = os.system(cmd)

print("7. Copy the modified source files to new structure...")
'''There is a file that change the include to use.'''
#print("7.1 Copy mpas_atm_core_interface.F...")
#cmd = "cp "+monan_modified+"/mpas_atm_core_interface.F ./monan/src/core_atmosphere/"
#returned_value = os.system(cmd)
#print("7.2 Copy mpas_init_atm_core_interface.F...")
#cmd = "cp "+monan_modified+"/mpas_init_atm_core_interface.F ./monan/src/core_init_atmosphere/"
#returned_value = os.system(cmd)

print("8. Copy the others includes from github to include dir...")
'''There a lot of includes (.h, .inc) in aux directories
who needs to be copied to include dir. In future, if FYPP works 
with fpm this issue will not be necessary.'''

url_smiol = "https://github.com/monanadmin/smiol/raw/master/include/"
print("8.1 Copy from "+url_smiol)
output_directory = "./monan/include/"
fnames = ["smiol.h","smiol_codes.inc","smiol_types.h","smiol_utils.h","smiol_codes_f90.inc","smiolf_put_get_var.inc"]
for fname in fnames:
   url = url_smiol+fname
   print("   getting "+fname)
   try:
      r = requests.get(url)
   except:
      print("Error in request!")
      sys.exit()
   open(output_directory+fname , 'wb').write(r.content)

url_ezxml = "https://github.com/monanadmin/EZXML/raw/main/include/"
print("8.2 Copy from "+url_ezxml)
fnames = ["ezxml.h"]
for fname in fnames:
   url = url_ezxml+fname
   print("   getting "+fname)
   try:
      r = requests.get(url)
   except:
      print("Error in request!")
      sys.exit()   
   open(output_directory+fname , 'wb').write(r.content)

url_esmf = "https://github.com/monanadmin/esmf_time_f90/raw/master/include/"
print("8.3 Copy from "+url_esmf)
fnames = ["ESMF_Macros.inc","ESMF_TimeMgr.inc","ESMF_TimeMgr_f90.inc"]
for fname in fnames:
   print("   getting "+fname)
   url = url_esmf+fname
   try:
      r = requests.get(url)
   except:
      print("Error in request!")
      sys.exit()   
   open(output_directory+fname , 'wb').write(r.content)

print("9. Exchange Fortran pre -processor from cpp to fypp...")
'''Change all sources using the new fypp pre-processor commands instead cpp command.
At end all the fortran sources will be renamed to .F90
'''
changeDefines("./monan")

print("10. Moving mpas.F90, the main program, to ./monan/app/main.f90...")
'''FPP use the main program, called main, in app directory. The main program
don't have pre-processor directives. Then it will be put in app with .f90
extension instead .F90
'''
cmd = "mv ./monan/src/driver/mpas.F90 ./monan/app/main.f90"
write_log(cmd)
returned_value = os.system(cmd)

print("11. Renaming the src directory to pre_build_src for be used in fypp...")
'''The FYPP will be filter pre_build_src to src using the defines that user
give to script in setup/monan_setup.toml'''
cmd = "mv ./monan/src ./monan/pre_build_src"
write_log(cmd)
returned_value = os.system(cmd)

print("12. Copy the monan_setup.toml to setup directory...")
'''The monan_setup.toml have the instruction to configure the fpm build the MONAN model
and filter using FYPP the pre-build creating src code.'''
cmd = "cp "+monan_setup+" ./monan/setup/monan_setup.toml"
write_log(cmd)
returned_value = os.system(cmd)

print("12. Copy the xml to setup directory...")
'''The xml will indicate how to run the model.'''
cmd = "cp ./monan/pre_build_src/core_atmosphere/Registry.xml ./monan/setup/core_atmosphere"
write_log(cmd)
returned_value = os.system(cmd)
cmd = "cp ./monan/pre_build_src/core_init_atmosphere/Registry.xml ./monan/setup/core_init_atmosphere"
write_log(cmd)
returned_value = os.system(cmd)
cmd = "cp ./monan/pre_build_src/core_atmosphere/diagnostics/*.xml ./monan/setup/core_atmosphere/diagnostics"
write_log(cmd)
returned_value = os.system(cmd)

print("13. Copy the fpm.toml to main directory...")
'''The fpm.toml is the file used by fpm to create the code.'''
cmd = "cp "+monan_fpm+" ./monan/fpm.toml"
write_log(cmd)
returned_value = os.system(cmd)

print("14. Copy all pre_build files to monan/scripts...")
'''Pre_build files are used to precompile and filter the sources accordingly monan_setup.toml.'''
cmd = "cp "+monan_scripts+"/*.py ./monan/scripts"
write_log(cmd)
returned_value = os.system(cmd)

print("15. Copy the README.md...")
'''README is necessary by github.'''
cmd = "cp "+monan_readme+" ./monan"
write_log(cmd)
returned_value = os.system(cmd)

print("16. Modify module_bl_ysu.F90 to adapt FYPP...")
fm = open("./monan/pre_build_src/core_atmosphere/physics/physics_wrf/module_bl_ysu.F90","r")
filedata = fm.read()
filedata = filedata.replace("${NEED_B4B_DURING_CCPP_TESTING}$","NEED_B4B_DURING_CCPP_TESTING")
fm.close()
fm = open("./monan/pre_build_src/core_atmosphere/physics/physics_wrf/module_bl_ysu.F90","w")
fm.write(filedata)
fm.close()

print("17. Modify mpas_io_F90 to Fortran include...")
fm = open("./monan/pre_build_src/framework/mpas_io.F90","r")
filedata = fm.read()
filedata = filedata.replace("smiol_codes.inc","smiol_codes_f90.inc")
fm.close()
fm = open("./monan/pre_build_src/framework/mpas_io.F90","w")
fm.write(filedata)
fm.close()

print("18. Modify mpas_atm_time_integration.F90 to exclude conflict...")
fm = open("./monan/pre_build_src/core_atmosphere/dynamics/mpas_atm_time_integration.F90","r")
filedata = fm.read()
filedata = filedata.replace("real (kind=RKIND), parameter, private :: seconds_per_day = 86400.0_R","!real (kind=RKIND), parameter, private :: seconds_per_day = 86400.0_R")
fm.close()
fm = open("./monan/pre_build_src/core_atmosphere/dynamics/mpas_atm_time_integration.F90","w")
fm.write(filedata)
fm.close()

print("All  done! MONAN strucuture ready to start!")

pbl.close()



