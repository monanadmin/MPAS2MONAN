import os
from datetime import datetime

def write_Filter_log(message,pbl):
   now = datetime.now()
   dt_string = now.strftime("%Y%m%d%H%M%S")
   pbl.write("{0} {1}\n".format(dt_string,message))

def filterFile(root,file,cpp,fpp,new_src):
   #Open a log file to write the steps
   pbl = open("filter.log","a")
   write_Filter_log("filter "+root+" in "+new_src,pbl)

   print("Filtering "+root+"/"+file)
   file_name,file_ext  = os.path.splitext(file)
   print(file_name,"|",file_ext)
   if file_ext == ".F90":
      fileDestin = file_name +".f90"
   elif file_ext == ".fypp":
      fileDestin = file_name+".inc"
   elif file_ext == ".h" or file_ext == ".inc":
      return
      #fileDestin = file[0:-2]+".tmp"
   elif file == "Registry.xml":
      fileDestin = "Registry_processed.xml"
   else:
      fileDestin = file

   if file_name == "smiol_codes":
      cmd = "mv {0}/{1} {2}/{3}".format(root,file,root,fileDestin)
   elif file_ext == ".F90" or file_ext == ".xml" or file_ext == ".fypp":
      cmd = "{0} {1}/{2} {3}/{4}".format(fpp,root,file,new_src,fileDestin)
      write_Filter_log(cmd,pbl)
   else:
      cmd = "{0} {1}/{2} {3}/{4}".format(cpp,root,file,new_src,fileDestin)
      write_Filter_log(cmd,pbl)
   returned_value = os.system(cmd)
   if returned_value != 0:
      print("Err ({0}) in command {1}".format(returned_value,cmd))
      write_Filter_log("Err ({0}) in command {1}".format(returned_value,cmd),pbl)
      exit(-1)
   
   if file_ext == ".h":
      cmd = "mv {0}/{1} {2}/{3}".format(root,fileDestin,root,file)
      write_Filter_log(cmd,pbl)
      returned_value = os.system(cmd)

   pbl.close()


def filterFypp(monan_base_dir,cpp,fpp):

   for root, dirs, files in os.walk(monan_base_dir):
      #print("root=",root)
      if "pre_build_src" in monan_base_dir:
         new_src = root.replace("pre_build_src","src")
      else:
         new_src = root
      for file in files:
         filterFile(root,file,cpp,fpp,new_src)



   
