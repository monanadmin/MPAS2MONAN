"""allStreams.py
   Description: This python script write all the streams
   inputs:
     abrev - abreviation of atmosphere, init-atmosphete, ocean, etc
     root - Data read from Registry_processed.xml
"""
__author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
__copyright__   = "Copyright 2023, Monan Model"

# Python functions
import xml.etree.ElementTree as ET
import sys

def streams_write(fileName):
   """Faz a leitura do arquivo xml obtendo seu conteúdo na estrutura"""
   tree = ET.parse(fileName)
   root = tree.getroot()

   core = root.attrib["core"]

   sectors = ["nhyd_model", "damping", "limited_area", "io", "decomposition", "restart", "printout",
            "IAU", "physics", "assimilation", "development","soundings"  ]

   st_atmosphere = open("streams.{0}".format(core),"w")
   """Escreve a abertura do streams atmosphere"""
   st_atmosphere.write("<streams>\n")

   """
   A variável config_do_restart controla se será ou não criado o stream list 'restart'.
   Se <nml_option name="config_do_restart" tem default_value="true" o stream será escrito
   """
   config_do_restart = False # Essa variável controla 
   """
   A variável iau controla se será ou não criado o stream list 'iau'.
   Se <nml_option name="config_IAU_option" tem default_value diferente de "off" o stream iau será gerado
   """
   iau = False
   """
   A variável lbc controla se será ou não criado o stream list 'lbc'.
   Se <nml_option name="config_apply_lbcs" tem default_value diferente de "false" o stream lbc será gerado.
   """
   lbc = False

   """ o laço abaixo percorre o XML pegando as definições da raiz (primeiro nível)"""
   for child in root:
      """Se a definição é namelist (<nml_record) e o atributo in_defaults for verdadeiro então ele deve ser processado para extrair as tags"""
      if child.tag == "nml_record" and child.attrib["in_defaults"] == "true": 
         if child.attrib["name"] in sectors: #Se existe o setor do namelist na lista de setores
            """percorre todo a estrutura do XML para verificar as tags"""
            for gran_child in child:
               """Se for uma tag de namelist, nml_option, então os elementos devem ser percorridos"""
               if gran_child.tag == "nml_option":
                  """ Se estiver ligado o "in_defaults" é preciso verificar se é verdadeiro, ex:
                  <nml_option name="config_time_integration" ... in_defaults="false
                  No caso exemplo acima existe in_defaults mas é falso """
                  if "in_defaults" in gran_child.attrib:
                     """Verifica se o in_defaults não é falso"""
                     if gran_child.attrib["in_defaults"] != "false":
                        """O trecho abaixo apenas avalia os possíveis streams:"""
                        """Verifica se é um restart e determina se deve ou não fazer o stream"""
                        if child.attrib["name"] == "restart":
                           if gran_child.attrib["name"] == "config_do_restart" and gran_child.attrib["default_value"] != "false":
                                 config_do_restart = True
                        """Verifica se é um IAU e determina se deve ou não fazer o stream"""
                        if child.attrib["name"] == "IAU":
                           if gran_child.attrib["name"] == "config_IAU_option" and gran_child.attrib["default_value"] != "off":
                                 iau = True
                        """Verifica se é um LBC e determina se deve ou não fazer o stream"""
                        if child.attrib["name"] == "limited_area":
                           if gran_child.attrib["name"] == "config_apply_lbcs" and gran_child.attrib["default_value"] != "false":
                                 lbc = True
                  else:
                     """ Se NÃO estiver ligado o "in_defaults" então considera-se que é para produzir o namelist
                     Repete-se a mesma estrutura do trecho acima para a geração das flags config_do_restart, iau e lbc
                      e também para escrita do namelist """

                     if child.attrib["name"] == "restart":
                        if gran_child.attrib["name"] == "config_do_restart" and gran_child.attrib["default_value"] != "false":
                                 config_do_restart = True
                     if child.attrib["name"] == "IAU":
                        if gran_child.attrib["name"] == "config_IAU_option" and gran_child.attrib["default_value"] != "off":
                           iau = True
                     if child.attrib["name"] == "limited_area":
                        if gran_child.attrib["name"] == "config_apply_lbcs" and gran_child.attrib["default_value"] != "false":
                           lbc = True

      """ Chama a função streams que vai tratar da verificação e geração dos streams a serem gerados"""
      streams(child,st_atmosphere,config_do_restart,iau,lbc)
   """ Escreve o fechamento das streams e fecha os arquivos ainda abertos"""
   st_atmosphere.write("</streams>\n")
   st_atmosphere.close()
   return


def streams(child,st_atmosphere,config_do_restart,iau,lbc):
   """streams: Sail in child attributes for each stream defined.
   
   inputs : child (estrutura com o nível 1 do xml), st_atmosphere: arquivo aberto
   outputs: Não retorna nada 
   
   """
   __author__      = "Rodrigues, L. F. [LFR] luizfrodrigues@protonmail.com"
   __copyright__   = "Copyright 2023, Monan Model"


   """FASE 1: Essa fase da função trata de fazer a escrita do arquivo "streams.atmosphere" que
   tem internamente uma configuração de XML com suas tags.
   -------------------------------------------------------------------------------------------"""

   """ A variável nim determina se foi declarado uma tag 'not' immutable
   Essa tag é definida nas seções de stream  do XML <stream name="input" e possuem uma tag immutable="false"
   """
   nim = False 
   """Verifica se a tag nível 1 é "streams" e se for faz o tratamento"""
   if child.tag == "streams":
      """Percorre o nível 2 e obtém as tags"""
      for gran_child in child:
         """Se a tag for stream trata essa tag adequadamente"""
         if gran_child.tag == "stream":
            """O stream.atmosphere define dois tipos de stream em sua estrutura:
               <stream... e <immutable_stream...
               O immutable é declarado quando a tag immutable="true" está nos atributos
            """
            if "immutable" in gran_child.attrib:
               """Se o atributo for true acrescenta "immutable_" precedendo o stream"""
               if gran_child.attrib["immutable"] == "true":
                  st_atmosphere.write("   <immutable_stream name='{0}'\n".format(gran_child.attrib["name"]))
                  nim = False
                  """ Caso não seja immutable é escrito apenas stream name"""
               else:
                  nim = True
                  st_atmosphere.write("   <stream name='{0}'\n".format(gran_child.attrib["name"]))
            else: 
               """ Caso não seja immutable é escrito apenas stream name"""
               nim = True
               st_atmosphere.write("   <stream name='{0}'\n".format(gran_child.attrib["name"]))
            """ nel é o número de atributos (elementos) total dentro da tag"""
            nel = len(gran_child.attrib.keys())
            """nc é uma contagem de elementos"""
            nc = 0
            """Percorre todos os elementos em um laço"""
            for elem in gran_child.attrib:
               """Incrementa o número de elementos lidos. Pode haver mais ou menos elementos 
               dependendo de cada tag."""
               nc = nc + 1
               """Os elementos name e immutable já foram usados na escrita do nome do stream
               Não são mais necessários e nada é feito"""
               if elem=="name" or elem=="immutable":
                  continue
               else:
                  """Os demais elementos que compõe a tag devem ser escritos. Todos os elementos são
                  escritos linha a linha. O penúltimo deles (antes de immutable) recebe o fechamento
                  da tag "/>" """
                  if nc < nel-1:
                     st_atmosphere.write("      {0} ='{1}'\n".format(elem,gran_child.attrib[elem]))
                  elif nc == nel-1:
                     st_atmosphere.write("      {0} ='{1}' />\n".format(elem,gran_child.attrib[elem]))
                     """Se não é um immutable é preciso fechar a tag geral do arquivo com um </stream>"""
                     if nim == True:
                        nim = False
                        st_atmosphere.write("   </stream>\n")

            """FASE 2: Essa fase da função produz os diversos stream lists.
            As streams surface, output e diagnostics sempre serão produzidas.
            As streams restart, iau e lbc dependem das variáveis lógicas config_do_restart, iau e lbc estarem True.
            Cada uma das partes abaixo abre um arquivo de stream que contém apenas a lista de variáveis, arrays ou
            structs que devem ser objeto de leitura ou escrita pelo modelo.
            -------------------------------------------------------------------------------------------"""

            if gran_child.attrib["name"] == "surface": 
               stream_surface = open("stream_list.atmosphere.surface", "w")
               for gran_gran_child in gran_child:
                  if gran_gran_child.tag == "var":
                    stream_surface.write("{0}\n".format(gran_gran_child.attrib["name"]))
               stream_surface.close()
            
            if gran_child.attrib["name"] == "output": 
               stream_output = open("stream_list.atmosphere.output", "w")
               for gran_gran_child in gran_child:
                  if gran_gran_child.tag == "var" or gran_gran_child.tag == "var_array":
                    stream_output.write("{0}\n".format(gran_gran_child.attrib["name"]))
               stream_output.close()                                    
            
            if gran_child.attrib["name"] == "diagnostics": 
               stream_diagnostics = open("stream_list.atmosphere.diagnostics", "w")
               for gran_gran_child in gran_child:
                  if gran_gran_child.tag == "var" or gran_gran_child.tag == "var_array":
                    stream_diagnostics.write("{0}\n".format(gran_gran_child.attrib["name"]))
               stream_diagnostics.close()
            
            if gran_child.attrib["name"] == "restart" and config_do_restart: 
               stream_restart = open("stream_list.atmosphere.restart", "w")
               for gran_gran_child in gran_child:
                  if gran_gran_child.tag == "var" or gran_gran_child.tag == "var_array":
                    stream_restart.write("{0}\n".format(gran_gran_child.attrib["name"]))
               stream_restart.close()               

            if gran_child.attrib["name"] == "iau" and iau: 
               stream_iau = open("stream_list.atmosphere.iau", "w")
               for gran_gran_child in gran_child:
                  if gran_gran_child.tag == "var" or gran_gran_child.tag == "var_struct":
                    stream_iau.write("{0}\n".format(gran_gran_child.attrib["name"]))
               stream_iau.close()        

            if gran_child.attrib["name"] == "lbc_in" and lbc: 
               stream_lbc = open("stream_list.atmosphere.lbc", "w")
               for gran_gran_child in gran_child:
                  if gran_gran_child.tag == "var" or gran_gran_child.tag == "var_array":
                    stream_lbc.write("{0}\n".format(gran_gran_child.attrib["name"]))
               stream_lbc.close()          
   return