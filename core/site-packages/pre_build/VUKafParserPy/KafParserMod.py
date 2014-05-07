########################################################################
# 14 Jan 2013: added function add_attrs_to_layer
########################################################################

###################
# List of changes #
###################
# 14 Jan 2013: added function add_attrs_to_layer
# 27 Feb 2013: added code for comply with DTD
# 18 Jun 2013: getSingleProperties adapted to the structure KAF/features/properties/property/references/span/target
# 18 Jun 2013: funcion add_property created for adding the properties to the KAF


from lxml import etree
from KafDataObjectsMod import *
import time

class KafParser:
  def __init__(self,filename=None):
	self.tree=None
	self.__pathForToken={}
	self.__term_ids_for_token_id = None
    
	if filename:
		self.tree = etree.parse(filename,etree.XMLParser(remove_blank_text=True))
		## Do the text tokenization
		self.__textTokenization()
	else:
		root = etree.Element('KAF')
		root.set('version','v1.opener')
		root.set('{http://www.w3.org/XML/1998/namespace}lang','en')
		self.tree = etree.ElementTree(element=root)
		
  def __textTokenization(self):
	for wf in self.tree.findall('text/wf'):
	  wid = wf.get('wid')
	  self.__pathForToken[wid] = self.tree.getpath(wf)
	 
  
  def getToken(self,tid):
	path = self.__pathForToken[tid]
	return self.tree.xpath(self.__pathForToken[tid])[0]

  
  def getLanguage(self):
	  lang = self.tree.getroot().get('{http://www.w3.org/XML/1998/namespace}lang','nl')
	  return lang
	  
  ## Return a list of (sentence_id, TOKENS) where tokens is a list of (token_id,token)
  ## [(s_id1, T1), (sent_id2, T2)....]
  ## T1 --> [(tokenid, token), (tokenid2,token2)....]
  def get_tokens_in_sentences(self):
      sents = []
      current = []
      previous_sent = None
      for element in self.tree.findall('text/wf'):
          w_id = element.get('wid')
          s_id = element.get('sent')
          word = element.text
          
          if previous_sent is not None and s_id != previous_sent:
              sents.append((previous_sent,current))
              current = []
          current.append((w_id,word))
          previous_sent = s_id
      ####
      sents.append((s_id,current)) 
      return sents
  
  def get_term_ids_for_token_id(self,tok_id):
      if self.__term_ids_for_token_id is None:
          self.__term_ids_for_token_id = {}
          for element in self.tree.findall('terms/term'):
              term_id = element.get('tid')
              for target in element.findall('span/target'):
                  token_id = target.get('id')
                  if token_id not in self.__term_ids_for_token_id:
                      self.__term_ids_for_token_id[token_id] = [term_id]
                  else:
                      self.__term_ids_for_token_id[token_id].append(term_id)
      return self.__term_ids_for_token_id.get(tok_id,[])
  
          
      
  def getTokens(self):
	for element in self.tree.findall('text/wf'):
	  w_id = element.get('wid')
	  s_id = element.get('sent','0')
	  word = element.text
	  yield (word, s_id, w_id)
	
    
    
  def getTerms(self):
	 if self.tree:
	   for element in self.tree.findall('terms/term'):
		   kafTermObj = KafTerm()
		   kafTermObj.setId(element.get('tid'))
		   kafTermObj.setLemma(element.get('lemma'))
		   kafTermObj.setPos(element.get('pos'))
		   kafTermObj.morphofeat = element.get('morphofeat')
		   		   
		   ## Parsing sentiment
		   sentiment = element.find('sentiment')
		   if sentiment is not None:
			 resource = sentiment.get('resource','')
			 polarity = sentiment.get('polarity',None)
			 strength = sentiment.get('strength','')
			 subjectivity = sentiment.get('subjectivity','')
			 sentiment_modifier = sentiment.get('sentiment_modifier')
			 
			 my_sent = KafTermSentiment()
			 my_sent.simpleInit(resource,polarity,strength,subjectivity,sentiment_modifier)
			 kafTermObj.setSentiment(my_sent)
		  
		   ## Parsing the span
		   span = element.find('span')
		   if span is not None:
			list_ids = [target.get('id') for target in span.findall('target')]
			kafTermObj.set_list_span_id(list_ids)
		
			 
		   yield kafTermObj
	 else:
	   return
	  
	  
  def getSentimentTriples(self):
	data = []
	if self.tree:
	  for term_element in self.tree.findall('terms/term'):
		lemma = term_element.get('lemma')
		polarity = None
		sentiment_modifier = None
		
		sentiment_element = term_element.find('sentiment')
		if sentiment_element is not None:
			polarity = sentiment_element.get('polarity',None)
			sentiment_modifier = sentiment_element.get('sentiment_modifier')
		data.append( (lemma,polarity,sentiment_modifier))
	return data
	  
   
	  
  def addPolarityToTerm(self,termid,my_sentiment_attribs,polarity_pos=None):
	if self.tree:
	  for element in self.tree.find('terms'):
		if element.get('tid','')==termid:
		  
		  #In case there is no pos info, we use the polarityPos
		  if not element.get('pos') and polarity_pos is not None:
			element.set('pos',polarity_pos)
		  sentEle = etree.Element('sentiment',attrib=my_sentiment_attribs)
		  element.append(sentEle)  
	  
  def saveToFile(self,filename,myencoding='UTF-8'):
	if self.tree:
	  self.tree.write(filename,encoding=myencoding,pretty_print=True,xml_declaration=True)
	  
  
  def addLinguisticProcessor(self,name,version, layer, time_stamp=True):
	aux = self.tree.findall('kafHeader')
	if len(aux)!=0:
	  kaf_header = aux[0]
	else:
	  kaf_header = etree.Element('kafHeader')
	  self.tree.getroot().insert(0,kaf_header)

        aux2= kaf_header.findall('linguisticProcessors')
        if len(aux2) == 0:
          new_lp = etree.Element('linguisticProcessors')
          new_lp.set('layer',layer)
          kaf_header.append(new_lp)
          
	## Check if there is already element for the layer
	my_lp_ele = None
	
	for element in kaf_header.findall('linguisticProcessors'):
	  if element.get('layer','')==layer:
		my_lp_ele = element
		break
	  
	if time_stamp:  
	  my_time = time.strftime('%Y-%m-%dT%H:%M:%S%Z')
	else:
	  my_time = '*'
	  
	my_lp = etree.Element('lp')
	my_lp.set('timestamp',my_time)
	my_lp.set('version',version)
	my_lp.set('name',name)

	if my_lp_ele is not None: #Already an element for linguisticProcessor with the layer
	  my_lp_ele.append(my_lp)
	else:
	  # Create a new element for the LP layer
	  my_lp_ele = etree.Element('linguisticProcessors')
	  my_lp_ele.set('layer',layer)
	  my_lp_ele.append(my_lp)
	  #my_lp_ele.tail=my_lp_ele.text='\n'
	  ## Should be inserted after the last linguisticProcessor element (stored in variable element)
	  idx = kaf_header.index(element)
	  kaf_header.insert(idx+1,my_lp_ele)
		
	  
  def addLayer(self,type,element,first_char_id=None):
	if first_char_id is None:
		first_char_id = type[0]
		
	## Check if there is already layer for the type
	layer_element = self.tree.find(type)
	
	if layer_element is None:
	  layer_element = etree.Element(type)
	  self.tree.getroot().append(layer_element)
	  ## The id is going to be the first one
	  new_id = first_char_id+'1'
	else:
	  ## We need to know how many elements there are in the layer
	  current_n = len(layer_element.getchildren())
	  new_id = first_char_id+''+str(current_n+1)
	  
	  
	## In this point layer_element points to the correct element, existing or created
	
	element.set(first_char_id+'id',new_id)
	layer_element.append(element)
	return new_id
	
  def addElementToLayer(self,layer, element,first_char_id=None):
	return self.addLayer(layer,element,first_char_id)

  def add_attrs_to_layer(self,layer,attrs):
	layer_element = self.tree.find(layer)
	if layer_element is not None:
	  for att, val in attrs.items():
		layer_element.set(att,val)
		

  def addAttributeToElement(self,path,str_id, id, attribute, value,sub_path=None):
	  for element in self.tree.findall(path):
		if id is not None and element.get(str_id,None) == id:
		  if sub_path is not None:
			elements = element.findall(sub_path)
			if len(elements)!=0: element = elements[0]
		  element.set(attribute,value)
		  return

  
  ## This works with the original definition of the property layer
  ## KAF -> properties -> property* -> span* -> target*
  def getSingleProperties_old(self):
	  for element in self.tree.findall('properties/property'):
		  my_id = element.get('pid')
		  my_type = element.get('type')
		  ref = element.find('references')
		  if ref is not None:
			element = ref
		  for span_element in element.findall('span'):
			  target_ids = [target_element.get('id') for target_element in span_element.findall('target')]
			  my_prop = KafSingleProperty(my_id,my_type,target_ids)
			  yield my_prop
			   
  ## 18-June-2013
  def getSingleProperties(self):
	  for property in self.tree.findall('features/properties/property'):
		  my_id = property.get('pid')
		  if my_id is None:
			  my_id = property.get('fpid')
		  my_type = property.get('lemma')
		  for span_element in property.findall('references/span'):
			  target_ids = [target_element.get('id') for target_element in span_element.findall('target')]
			  my_prop = KafSingleProperty(my_id,my_type,target_ids)
			  yield my_prop

  # This function adds a new property of the type given with the list of ids given
  # my_type -> 'sleeping comfort'	list_ids = ['id1','id2']
  # It creates the features/properties layers in case 
  # Agglomerates all the properties for the same TYPE under the same property element
  # It calculates automatically the number for the identifier depending on the number
  # of properties existing
  def add_property(self,my_type,list_ids,comment=None):
      
      #Looking for feature layer or creating it
      feature_layer = self.tree.find('features')
      if feature_layer is None:
          feature_layer = etree.Element('features')
          self.tree.getroot().append(feature_layer)
          
      #Looking for properties layer
      properties_layer = feature_layer.find('properties')
      if properties_layer is None:
          properties_layer = etree.Element('properties')
          feature_layer.append(properties_layer)
          
      num_props = 0
      property_layer = None
      for property in properties_layer.findall('property'):
          num_props += 1
          prop_type = property.get('lemma')
          if prop_type == my_type:
              property_layer = property
              break
          
      if property_layer is None:  # There is no any property for that type, let's create one
          property_layer = etree.Element('property')
          property_layer.set('pid','p'+str(num_props+1))
          property_layer.set('lemma',my_type)    
          properties_layer.append(property_layer)
          
          
      references = property_layer.find('references')
      if references is None:
          references = etree.Element('references')
          property_layer.append(references)
      ## Create the new span
      if comment is not None:
        references.append(etree.Comment(comment))
      span = etree.Element('span')
      references.append(span)
      for my_id in list_ids:
           span.append(etree.Element('target',attrib={'id':my_id}))
       
   
			  
  
  def getSingleEntities(self):
	  for element in self.tree.findall('entities/entity'):
		  my_id = element.get('eid')
		  my_type = element.get('type')
		  my_path_to_span = None
		  ref = element.find('references')
		  if ref is not None:
                      my_path_to_span = 'references/span'
                  else:
                      my_path_to_span = 'span'

		  for span_element in element.findall(my_path_to_span):
			  target_ids = [target_element.get('id') for target_element in span_element.findall('target')]
			  my_prop = KafSingleEntity(my_id,my_type,target_ids)
			  yield my_prop


  def getOpinions(self):
	for element in self.tree.findall('opinions/opinion'):
	  my_id = element.get('oid')
	  
	  tar_ids_hol = []
	  tar_ids_tar = []
	  polarity = strenght = ''
	  tar_ids_exp = []
	  
	  #Holder
	  opi_hol_eles = element.findall('opinion_holder')
	  if len(opi_hol_eles)!=0:
		  opi_hol_ele = opi_hol_eles[0]
		  tar_ids_hol = [t_ele.get('id') for t_ele in opi_hol_ele.findall('span/target')]
	  
	  #Target
	  opi_tar_eles = element.findall('opinion_target')
	  if len(opi_tar_eles) != 0:
		opi_tar_ele = opi_tar_eles[0]
		tar_ids_tar = [t_ele.get('id') for t_ele in opi_tar_ele.findall('span/target')]
		
	  ## Opinion expression
	  opi_exp_eles = element.findall('opinion_expression')
	  if len(opi_exp_eles) != 0:
		  opi_exp_ele = opi_exp_eles[0]
		  polarity = opi_exp_ele.get('polarity','')
		  strength = opi_exp_ele.get('strength','')
		  tar_ids_exp = [t_ele.get('id') for t_ele in opi_exp_ele.findall('span/target')]

	  yield KafOpinion(my_id,tar_ids_hol, tar_ids_tar, KafOpinionExpression(polarity, strength,tar_ids_exp))


  
  def remove_opinion_layer(self):
      opinion_layer = self.tree.find('opinions')
      if opinion_layer is not None:
          self.tree.getroot().remove(opinion_layer)
  
  ## This function add an opinion to the opinion layer, creating it if does not exist
  ## The id is calculated automatically according to the number of elements and ensring there is no repetition
  def add_opinion(self,hol_ids,tar_ids,polarity,strength,exp_ids):
      
      #Looking for opinion layer or creating it
      opinion_layer = self.tree.find('opinions')
      if opinion_layer is None:
          opinion_layer = etree.Element('opinions')
          self.tree.getroot().append(opinion_layer)
          
      ## Generating unique id
      list_of_oids = [opi.get('oid') for opi in opinion_layer]
      
      n = 1
      while True:
          my_id = 'o'+str(n)
          if my_id not in list_of_oids:
              break
          n += 1
      #####
          
      op_ele = etree.Element('opinion')
      opinion_layer.append(op_ele)
      op_ele.set('oid',my_id)

      ## Holder
      op_hol = etree.Element('opinion_holder')
      op_ele.append(op_hol)
      span_op_hol = etree.Element('span')
      op_hol.append(span_op_hol)
      for my_id in hol_ids:
        span_op_hol.append(etree.Element('target',attrib={'id':my_id}))

      ## TARGET
      op_tar = etree.Element('opinion_target')
      op_ele.append(op_tar)
      span_op_tar = etree.Element('span')
      op_tar.append(span_op_tar)
      for my_id in tar_ids:
        span_op_tar.append(etree.Element('target',attrib={'id':my_id}))

      ## Expression
    
      op_exp = etree.Element('opinion_expression',attrib={'polarity':polarity,
                                                       'strength':str(strength)})
      op_ele.append(op_exp)
      span_exp = etree.Element('span')
      op_exp.append(span_exp)
      for my_id in exp_ids:
        span_exp.append(etree.Element('target',attrib={'id':my_id}))



	
	
