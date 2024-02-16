def parse_line(line,file):
   #print(line)
   line = line.rstrip()
   len_line=len(line)
   try:
      openParentheses_pos = line.index("(")
   except:
      print("line error!","|"+line+"|")
      exit()
   prefix = line[:openParentheses_pos]
   closeParentheses_pos = line.rfind(")")
   sufix = line[closeParentheses_pos+1:]
   arguments = line[openParentheses_pos+1:closeParentheses_pos].strip()
   parse = arguments.split(",")
   for i in range(len(parse)):
      parse[i] = parse[i].strip()
   #if "module_ra_rrtmg_lw" in file:
   #   print("in parse_line:",prefix," -- |",arguments[0].strip(),"| -- ",sufix,"A"==arguments[0])
   return prefix,sufix,parse

def replace_values(list_to_replace, item_to_replace, item_to_replace_with):
   return [item_to_replace_with if item == item_to_replace else item for item in list_to_replace]

def create_line(prefix,vars_in_call,file,control):
   line = prefix+"("
   nvars = len(vars_in_call)
   count = 0
   #if "module_ra_rrtmg_lw" in file:
   #   print("In create_line:",vars_in_call,nvars)
   for var in vars_in_call:
      count = count + 1
      if count == nvars:
         if control==0:
            line = line+var
         else:
            line = line+var+")"
      else:
         line = line+var+","
   return line

def isArray(var):
   if "(" in var and ")" in var:
      return True
   else:
      return False
   
def check_arrays(var,file):
   if isArray(var):
      varName,sufix,vars_in_array = parse_line(var,file)
      #if "module_ra_rrtmg_lw" in file:
      #   print("in check arrays:",varName," -- |",vars_in_array,"| -- ",sufix)
      for v in vars_in_array:
         vars_in_array = replace_values(vars_in_array,v,"${"+v+"}$)"+sufix)
      #if "module_ra_rrtmg_lw" in file:
      #   print("2.",varName,vars_in_array) 
      array = create_line(varName,vars_in_array,file,0)
   else:
      array = var
   
   return array

def translate_fypp_call(allVars,line,file):
   #allVars = ['A']
   #line = "    call mpas_dmpar_bcast_reals(dminfo,size(A),A,data)"
   prefix,sufix,vars_in_call = parse_line(line,file)

   #print(vars_in_call)
   #print(prefix)

   for i in range(len(allVars)):
      vars_in_call[i] = vars_in_call[i].strip()
   #if "module_ra_rrtmg_lw" in file:
   #   print("apos strip:",vars_in_call)
   for var in allVars:
      vars_in_call = replace_values(vars_in_call,var,"${"+var+"}$")
   #if "module_ra_rrtmg_lw" in file:
   #   print("Apos: ",vars_in_call)   
   #print("vars_in_call=",vars_in_call)

   for var in vars_in_call:
      #print("var:",  var)
      vars_in_call = replace_values(vars_in_call,var.strip(),check_arrays(var.strip(),file))
   #   vars_in_call = replace_values(vars_in_call,var,"${"+var+"}$")
   #if "module_ra_rrtmg_lw" in file:
   #   print("Laco: ",vars_in_call)   

   line_to_print = create_line(prefix,vars_in_call,file,1)
   #print("line final: ",line_to_print)
   return line_to_print


