"""streams_gen.py
   Description: This python script namelist

        USAGE: python ./streams_gen.py registry_file streams_file_output stream_file_prefix stream_order [key1=value1] [key2=value2]......
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2024, Monan Model"

#../Registry_processed.xml streams.atmosphere stream_list.atmosphere. listed

# Python functions
import xml.etree.ElementTree as ET
import sys

SINGLE  = 0
SEPARATE = 1
ORDER_LISTED = 0
ORDER_MUTABLE = 1
spacing = " "*18

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

def generate_streams(root, fout, stream_file_prefix, order, attrs):
   fout.write("<streams>\n")
   if order == ORDER_MUTABLE:
      for child in root:
         if child.tag == "streams":
            print("child=",child["name"])
            for grand_child in child:
               if grand_child.tag == "stream":
                  write_stream = is_structure_writable(grand_child,attrs)
                  print(grand_child["name"])
                  if write_stream == False:
                     continue
                  if "immutable" in grand_child.keys():
                     if grand_child["immutable"] == "true":
                        write_stream_header(grand_child, fout)

   for child in root:
      if child.tag == "streams":
         for grand_child in child:
            if grand_child.tag == "stream":
               print("keys=",grand_child.keys())
               name = grand_child.attrib["name"]
               runtime = ""
               if "runtime_format" in grand_child.keys():
                  runtime = grand_child.attrib["runtime_format"]
               if "immutable" in grand_child.keys():
                  immutable = grand_child.attrib["immutable"]
               else:
                  immutable = ""
               write_stream = is_structure_writable(grand_child,attrs)
               if order == ORDER_LISTED:
                  if "immutable" in grand_child.keys():
                     if grand_child.attrib["immutable"] == "true" and write_stream:
                        write_stream_header(grand_child, fout)

               if immutable == "" or immutable != "" and grand_child.attrib["immutable"] == "false":
                  if runtime == "":
                     print(" Stream {0} requires the runtime_format attribute.\n".format(name))
                     sys.exit()
                  if runtime == "single_file":
                     filetype = SINGLE
                  elif runtime == "separate_file":
                     filetype = SEPARATE
                     filename = "{0}{1}".format(stream_file_prefix, name)
                  else:
                     print(" Stream {0} has attribute runtime_format set to an invalid option: {1}\n".format(name, runtime))

                  stream_written = False
                  write_stream = is_structure_writable(grand_child,attrs)

                  if write_stream:
                     write_stream_header(grand_child, fout)
                     stream_written = True
                     if filetype == SEPARATE:
                        fout.write("{0}<file name=\"{1}\"/>\n".format(spacing,filename))
                        fd2 = open(filename,"w")

                  ##Extract all streams from within the stream.
                  for member_xml in grand_child:
                     if member_xml.tag == "stream":
                        write_member = is_structure_writable(member_xml,attrs)
                        if write_member or (not write_member and write_stream):
                           if not stream_written:
                              write_stream_header(member_xml, fd)
                              stream_written = True
                              if filetype == SEPARATE:
                                 fout.write("\t<file name=\"{0}\"/>\n".format(filename))
                                 fd2 = open(filename,"w")

                        subname = member_xml.attrib["name"]
                        varpackages = ""
                        if varpackages in member_xml:
                           varpackages = member_xml.attrib["packages"]
                        
                        if varpackages == "":
                           fout.write("\t<stream name=\"{0}\"/>\n".format(subname))
                        else:
                           fout.write("\t<stream name=\"{0}\" packages=\"{1}\"/>\n".format(subname, varpackages))

                  # Extract all var_arrays from within the stream.
                  for member_xml in grand_child:
                     if member_xml.tag == "var_array":
                        write_member = is_structure_writable(member_xml,attrs)
                        if write_member or (not write_member and write_stream):
                           if not stream_written:
                              write_stream_header(member_xml, fout)
                              stream_written = True
                              if filetype == SEPARATE:
                                 fout.write("\t<file name=\"{0}\"/>\n".format(filename))
                                 fd2 = open(filename,"w")

                           subname = member_xml.attrib["name"]
                           varpackages = ""
                           if varpackages in member_xml:
                              varpackages = member_xml.attrib["packages"]

                           if filetype == SINGLE:
                              if varpackages == "":
                                 fout.write("\t<var_array name=\"{0}\"/>\n".format(subname))
                              else:
                                 fout.write("\t<var_array name=\"{0}\" packages=\"{1}\"/>\n".format(subname, varpackages))
                           elif filetype == SEPARATE:
                              fd2.write("{0}\n".format(subname))
                              if varpackages == "":
                                 print("Warning: Unable to add packages \"{0}\" to var_array \"{1}\" in stream \"{2}\" because runtime_format=separate_file\".\n".format(varpackages, subname, name))

                  # Extract all vars from within the stream.
                  for member_xml in grand_child:
                     if member_xml.tag == "var":
                        write_member = is_structure_writable(member_xml,attrs)
                        if write_member or (not write_member and write_stream):
                           if not stream_written:
                              write_stream_header(member_xml, fout)
                              stream_written = True                              
                              if filetype == SEPARATE:
                                 fout.write("\t<file name=\"{0}\"/>\n".format(filename))
                                 fd2 = open(filename,"w")   
                           subname = member_xml.attrib["name"]

                           varpackages = ""
                           if varpackages in member_xml:
                              varpackages = member_xml.attrib["packages"]   

                           if filetype == SINGLE:
                              if varpackages == "":
                                 fout.write("\t<var name=\"{0}\"/>\n".format(subname))
                              else:
                                 fout.write("\t<var name=\"{0}\" packages=\"{1}\"/>\n".format(subname, varpackages))
                           elif filetype == SEPARATE:
                              fd2.write("{0}\n".format(subname))
                              if varpackages == "":
                                 print("Warning: Unable to add packages \"{0}\" to var \"{1}\" in stream \"{2}\" because runtime_format=separate_file\".\n".format(varpackages, subname, name))

                  if stream_written:
                     fout.write("</stream>\n\n")
                     if filetype == SEPARATE:
                              fd2.close()

   fout.write("</streams>\n")

   return


def write_stream_header(child,fout):
#   		<stream name="restart" 
#                        type="input;output" 
#                        filename_template="restart.$Y-$M-$D_$h.$m.$s.nc" 
#                        input_interval="initial_only" 
#                        output_interval="1_00:00:00" 
#                        immutable="true">
   spacing = " "*18
   immutable = ""
   reference_time = ""
   filename_template = ""
   filename_interval = ""
   record_interval = ""
   clobber_mode = ""
   precision = ""
   io_type = ""
   packages = ""
   input_interval = ""
   output_interval = ""

   name = child.attrib["name"]
   type = child.attrib["type"]
   filename_template = child.attrib["filename_template"]
   if "filename_interval" in child.keys():
      filename_interval = child.attrib["filename_interval"]
   if "reference_time" in child.keys():
      reference_time = child.attrib["reference_time"]
   if "clobber_mode" in child.keys():
      clobber_mode = child.attrib["clobber_mode"]
   if "input_interval" in child.keys():
      input_interval = child.attrib["input_interval"]
   if "output_interval" in child.keys():
      output_interval = child.attrib["output_interval"]
   if "record_interval" in child.keys():
      record_interval = child.attrib["record_interval"]
   if "precision" in child.keys():
      precision = child.attrib["precision"]
   if "io_type" in child.keys():
      io_type = child.attrib["io_type"]
   if "immutable" in child.keys():
      immutable = child.attrib["immutable"]
   if "packages" in child.keys():
      packages = child.attrib["packages"]

   if immutable != "" and immutable == "true":
      fout.write("<immutable_stream name=\"{0}\"\n".format(name))
   else:
      fout.write("<stream name=\"{0}\"\n".format(name))
   fout.write('{0}type="{1}"'.format(spacing, type))
   if filename_template != "":
      fout.write("\n{0}filename_template=\"{1}\"".format(spacing, filename_template))
   if filename_interval != "":
      fout.write("\n{0}filename_interval=\"{1}\"".format(spacing, filename_interval))
   if reference_time != "":
      fout.write("\n{0}reference_time=\"{1}\"".format(spacing, reference_time))
   if record_interval != "":
      fout.write("\n{0}record_interval=\"{1}\"".format(spacing, record_interval))
   if clobber_mode != "":
      fout.write("\n{0}clobber_mode=\"{1}\"".format(spacing, clobber_mode))
   if precision != "":
      fout.write("\n{0}precision=\"{1}\"".format(spacing, precision))
   if io_type != "":
      fout.write("\n{0}io_type=\"{1}\"".format(spacing, io_type))
   if packages != "":
      fout.write("\n{0}packages=\"{1}\"".format(spacing, packages))
   if input_interval != "":
      fout.write("\n{0}input_interval=\"{1}\"".format(spacing, input_interval))
   if output_interval != "":
      fout.write("\n{0}output_interval=\"{1}\"".format(spacing, output_interval))
   if immutable != "" and immutable == "true":
      fout.write(" />\n\n")
   else:
      fout.write(" >\n\n")

   return



""" Main program ==========================================================="""
registry_file = sys.argv[1]
output_file = sys.argv[2]
stream_file_prefix = sys.argv[3]
stream_order = sys.argv[4]

if stream_order == "listed":
   order = ORDER_LISTED
elif stream_order == "mutable":
   order = ORDER_MUTABLE
else:
   print("\nError: Option {0} is not valid for stream order.\n", stream_order)
   print("\tOrder values are:\n")
   print("\t\tlisted -- Defines streams in the listed order in registry.\n")
   print("\t\tmutable -- Defines immutable streams first, followed by mutable streams.\n")
   sys.exit()

attrs = {}
#Getting the attributes to namelist
for item in sys.argv[5:]:
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

print("calling generate")
generate_streams(root, fout, stream_file_prefix, order, attrs)

fout.close()