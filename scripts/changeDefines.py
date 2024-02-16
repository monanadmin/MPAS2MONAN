#####!/usr/bin/python
"""@package docstring
Fortran Defines changing.

@author: Rodrigues, L.F. [LFR]
@e-mail: luizfrodrigues@protonmail.com
@date: 14Set2023

This program scan the directories and sub-directories passed and
change all #ifdef, #else, #endif to the fypp format, for example

instead 
   #ifdef SINGLE_PRECISION
we have
   #:if defined('SINGLE_PRECISION')

"""
import os
import sys
from parse_line import translate_fypp_call

#Read the directory structure and list all files
def recursive_file_gen(mydir):
    for root, dirs, files in os.walk(mydir):
        for file in files:
            yield os.path.join(root, file)

def change_preprocessor_phase1(file_in,file_out):
   with open(file_in,'r') as file:
      filedata = file.read()

      filedata = filedata.replace('#if defined',"#:if definol")
      filedata = filedata.replace('#if ( defined',"#:if definol(")
      filedata = filedata.replace('#if !defined','#:if not defined_2("")')
      filedata = filedata.replace('#if !(defined','#:if not defined_3("")')
      filedata = filedata.replace('#ifdef','#:if defined("")')
      filedata = filedata.replace('#ifndef','#:if not defined("")')
      filedata = filedata.replace('#endif','#:endif')      
      filedata = filedata.replace('#elif','#:elif')
      filedata = filedata.replace('#error','#:stop')
      filedata = filedata.replace('#if ','#:if ')
      filedata = filedata.replace('#if(','#:if (')
      filedata = filedata.replace('#else','#:else')
      filedata = filedata.replace('#define ','#:set ')
      filedata = filedata.replace('#include ','#:include ')
   with open(file_out,'w') as file:
      file.write(filedata)

def change_preprocessor_phase2(file_in,file_out):
   fin = open(file_in,"r")
   lines = fin.readlines()
   fout = open(file_out,"w")
   n_line = 0
   first = True
   for line in lines:
      n_line = n_line+1
      if line[0:12] == '#:if definol':
         var = line.split(")")[0].split("(")[1]
         newline = "#:if defined('"+var.strip()+"')"
         #print(newline)
         fout.write(newline+"\n")
         continue
      if line[0:16] == '#:if defined("")':
         newline = "#:if defined('"+line.split()[2]+"')"
         #print(newline)
         fout.write(newline+"\n")
         continue
      elif line[0:20] == '#:if not defined("")':
         newline = "#:if not defined('"+line.split()[3]+"')"
         fout.write(newline+"\n")
         continue
      elif line[0:22] == '#:if not defined_2("")':
         part1=line.split("(")[2]
         part=part1.split(")")[0]
         newline = "#:if not defined('"+part+"')"
         #print(newline)
         fout.write(newline+"\n")
         continue
      elif line[0:22] == '#:if not defined_3("")':
         part1=line.split("(")[2]
         part=part1.split(")")[0]
         newline = "#:if not defined('"+part+"')"
         #print(newline)
         fout.write(newline+"\n")
         continue
      elif line[0:5] == '#:if ' or line[0:6] == '#:elif':
         parts = line.split()
         #print("parts=",parts,len(parts))
         n_parts = len(parts)
         if n_parts == 2:
            newline = '#:if defined("'+parts[1]+'")'
            #print("Newline=",newline.strip())
            fout.write(newline+"\n")
            continue
         newline = line
         for char in "()":
            newline = newline.replace(char,"")
         if "defined" in newline and ("||" in newline or "&&" in newline):
            if "||" in newline:
               parts = newline.split("||")
               n_parts = len(parts)
               newline = ""
               parts_count = 0
               for part in parts:
                  parts_count = parts_count+1
                  if "defined" in part:
                     pos = part.index("defined")
                     var = part[pos+7:].strip()
                     part = 'defined("'+var+'")'
                     if parts_count < n_parts:
                        if parts_count == 1:
                           newline = "#:if " + part + " or "
                        else:
                           newline = newline.strip() + " " + part + " or "
                     else:
                        newline = newline.strip() + " " + part
                  else:
                     if parts_count < n_parts:
                        newline = newline.strip() + " " + part.strip() + " or "
                     else:
                        newline = newline.strip() + " " + part
            #print("new:",newline)
         fout.write(newline+"\n")
         continue
      elif line[0:6] == "#:set ":
         #print(line.strip())
         parse = line.split()
         #print(parse)
         if len(parse) == 3:
            newline = "#:set "+line.split()[1]
            #print(newline)
            li = len(newline)
            lf = len(line)
            newline = "{0} = '{1}'\n".format(newline,line[li:lf].strip())
         elif len(parse)== 2:
            newline = "#:set "+line.split()[1]+"\n"
         else:
            procedure = line.split()[1]
            newline = "#:def "+procedure+"\n   "+line[6+len(line.split()[1]):]+"#:enddef\n"
         fout.write(newline)
      else:
         fout.write(line)


def change_preprocessor_phase3(file_end,file_f90):
   fin = open(file_end,"r")
   lines = fin.readlines()
   fout = open(file_f90,"w")
   var_set = []
   call_set = []
   line_cnt = 0
   for line in lines:
      line_cnt = line_cnt + 1
      newline = line
      try:
         if(newline.strip()[0]=="!"):
            fout.write(newline)
            continue
      except:
            error = 1
      if line[0:6] == "#:set ":
         parse = line.split()
        # print ("parse=",parse,len(parse))
         if len(parse) == 4:
            var_set.append(parse[1])
            fout.write(newline)
            continue
      for var in var_set:
         if var in newline:
            newline = newline.replace(var,"${"+var+"}$")
      if line[0:6] == "#:def ":
         parse = line.split()
         call = parse[1]
         procedure = call.split("(")[0]
         if not procedure+"(" in call_set:
            call_set.append(procedure+"(")
         fout.write(newline)
         continue
      for proc in call_set:
         if proc in newline:
            newline = newline.replace(proc,"@:"+proc)
      newline = newline.replace("${${","${")
      newline = newline.replace("}$}$","}$")
      fout.write(newline)
   fin.close()
   fout.close()
   
def change_preprocessor_phase4(file_end,file_f90):
   fin = open(file_end,"r")
   lines = fin.readlines()
   fout = open(file_f90,"w")
   var_call = []
   line_cnt = 0
   check_var = False
   for line in lines:
      line_cnt = line_cnt + 1
      newline = line
      if "#:enddef" in newline:
            check_var = False
            fout.write(newline)
            continue
      try:
         if(newline.strip()[0]=="!"):
            fout.write(newline)
            check_var = False
            continue
      except:
            error = 1
      if line[0:6] == "#:def ":
         #print(line)
         check_var = True
         parse = line.split("(")[1]
         parse = parse.split(")")[0]
         vars = parse.split(",")
         #if "module_ra_rrtmg_lw" in file_end:
            #print(vars)
         #print("Fase4...:",line_cnt,newline.strip(),vars)
         fout.write(newline)
         continue
      


      if check_var:   
         if newline.strip()=="":
            fout.write(newline)
            continue
         newline = translate_fypp_call(vars,newline,file_end)
         #if "module_ra_rrtmg_lw" in file_end:
            #print("newline=",newline)
         fout.write(newline+"\n")
      else:
         fout.write(newline)

   fout.close()
   fin.close()


# def list_define(file_out,fm):
#    fin = open(file_out,"r")
#    lines = fin.readlines()
#    n_line = 0 
#    first = True
#    for line in lines:
#       n_line = n_line + 1
#       if line[0:6] == "#:def ":
#          if first:
#             message = "------ {0} ------\n".format(file_out)
#             fm.write(message)
#             first = False
#          message = "*{0:5d} {1}\n".format(n_line,line)
#          fm.write(message)
#          continue

def changeDefines(dir):

   list_files = list(recursive_file_gen(dir))

   for file_in in list_files:
      if file_in == "./monan/include/smiol_codes.inc":
         continue
      file_name,file_ext  = os.path.splitext(file_in)
      file_out = file_name+".aux"
      file_end = file_name+".F"
      file_int = file_name+".f90"
      if file_ext == ".F":
         file_f90 = file_name+".F90"
      elif file_ext == ".xml":
         file_f90 = file_name+".xml"
      elif file_ext == ".inc":
         file_f90 = file_name+".fypp"
      else:
         continue
      print("9.1 Doing: {0}".format(file_in))
      change_preprocessor_phase1(file_in,file_out)
      change_preprocessor_phase2(file_out,file_end)
      change_preprocessor_phase3(file_end,file_int)
      change_preprocessor_phase4(file_int,file_f90)
      # to fix a bug with FYPP - If the @: is after a ) the FYPP make a mistake
      if file_ext == ".F" or file_ext == ".F90":
         fi = open(file_f90,"r")
         fo = open("aux.F90","w")
         lines = fi.readlines()
         for line in lines:
            if ") @:" in line:
               pos = line.index(") @:")+2
               #print(file_f90,"|"+line+"|",pos)
               newline = line[0:pos]+" & \n"
               #print(newline)
               fo.write(newline)
               newline = " "*pos+line[pos:]
               fo.write(newline)
            else:
               newline = line
               fo.write(newline)
         fi.close()
         fo.close()
         cmd = "cp aux.F90 "+file_f90
         returned_value = os.system(cmd)
         cmd = "rm aux.F90 "
         returned_value = os.system(cmd)

      os.remove(file_out)
      os.remove(file_end)
      os.remove(file_int)
      if file_ext == ".inc":
         cmd = "rm "+file_in
         returned_value = os.system(cmd)

         


