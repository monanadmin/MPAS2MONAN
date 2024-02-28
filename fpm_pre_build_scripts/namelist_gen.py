"""generate_namelist.py
   Description: This python script namelist

        USAGE: python ./namelist_gen.py registry_file namelist_file_output [value_attribute] [key1=value1] [key2=value2]...
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2024, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def generate_namelist(root, fout, attrs):
   for child in root:
      if child.tag == "nml_record":
         #print(child.keys())
         if not is_structure_writable(child,attrs):
            continue
         recname = child.attrib["name"]
         #print(recname)
         fout.write("&"+recname+"\n")        
         for grand_child in child:
            if grand_child.tag == "nml_option":
               #print(grand_child.keys(),grand_child.attrib["name"])
               iswritable = is_structure_writable(grand_child,attrs)
               recname = grand_child.attrib["name"]
               if not iswritable:
                  continue
               if grand_child.attrib["type"] == "character":
                  fout.write('   {0} = "{1}"\n'.format(recname,grand_child.attrib["default_value"]))
               else:
                  fout.write("   {0} = {1}\n".format(recname,grand_child.attrib["default_value"]))

   return

def is_structure_writable(child,attrs):
   is_writable = []
   for at in attrs.keys():
      val_expected = attrs[at]
      #print(at,val_expected)
      if at in child.attrib.keys():
         if child.attrib[at] == val_expected:
            is_writable.append(True)
         else:
            is_writable.append(False)
      else:
         is_writable.append(True)
   if False in is_writable:
      return False
   else:
      return True


registry_file = sys.argv[1]
output_file = sys.argv[2]
attrs = {}
#Getting the attributes to namelist
for item in sys.argv[3:]:
   print(item)
   key,value = item.split("=")
   attrs.update({key:value})

"""Read xml and put in a structure tree"""
try:
   tree = ET.parse(registry_file)
except:
   print("Error: I can't parse file ",registry_file)
   print("Check if file exist!")
   sys.exit()
root = tree.getroot()

core = root.attrib["core"]
print("The CORE is '"+core+"'")

try:
   fout = open(output_file,"w")
except:
   print("Error: I can't create file ",output_file)
   print("Check if directory exist!")
   sys.exit()

generate_namelist(root, fout, attrs)

fout.close()

