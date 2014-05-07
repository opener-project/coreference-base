class KafTermSentiment:
  def __init__(self):
    self.resource=None
    self.polarity=None
    self.strength=None
    self.subjectivity=None
    
  def simpleInit(self,r,p,st,su,sm=None):
    self.resource=r
    self.polarity=p
    self.strength=st
    self.subjectivity=su
    self.sentiment_modifier = sm
    
  def getPolarity(self):
    return self.polarity
  
  def getSentimentModifier(self):
    return self.sentiment_modifier
    
    
class KafToken:
  def __init__(self,wid, value, sent=None, para=None):
    self.token_id = wid
    self.value = value
    self.sent = sent
    self.para = para
  

class KafOpinionExpression:
  def __init__(self,polarity,strength,targets):
    self.polarity = polarity
    self.strength = strength
    self.targets = targets
    
  def __str__(self):
    return 'Op_exp==> pol:'+self.polarity+' Str:'+self.strength+' ids:'+'-'.join(self.targets)
    
class KafOpinion:
  def __init__(self,id,holders, targets, opi_exp):
    self.id = id
    self.holders = holders
    self.targets = targets
    self.opi_exp = opi_exp
    
  def __str__(self):
    c='Opinion id'+self.id+'\n'
    c+='  Holders: '+'-'.join(self.holders)+'\n'
    c+='  Targets: '+'-'.join(self.targets)+'\n'
    c+=str(self.opi_exp)
    return c
    
    

class KafSingleProperty:
  def __init__(self,id,type,targets):
    self.id = id
    self.type = type
    self.targets = targets
    
    
  def get_id(self):
    return self.id
    
  def get_type(self):
    return self.type
  
  def get_span(self):
    return self.targets
  
  def __str__(self):
    return 'Id: '+self.id+' Type: '+self.type+' ids:'+' '.join(self.targets)


class KafSingleEntity:
  def __init__(self,id,type,targets):
    self.id = id
    self.type = type
    self.targets = targets
    
  def get_id(self):
    return self.id
    
  def get_type(self):
    return self.type
  
  def get_span(self):
    return self.targets
  
  def __str__(self):
    return 'Id: '+self.id+' Type: '+self.type+' ids:'+' '.join(self.targets)

class KafTerm:
  def __init__(self):
    self.tid = None
    self.lemma = None
    self.pos = None
    self.morphofeat = None
    self.sentiment = None
    self.list_span_id = []
    
  def get_morphofeat(self):
    return self.morphofeat
    
  def set_list_span_id(self, L):
    self.list_span_id = L
    
  def get_list_span(self):
    return self.list_span_id
    
  def get_polarity(self):
    if self.sentiment != None:
      return self.sentiment.getPolarity()
    else:
      return None
      
  def get_sentiment_modifier(self):
    if self.sentiment != None:
      return self.sentiment.getSentimentModifier()
    else:
      return None
    
    
  def setSentiment(self,my_sent):
    self.sentiment = my_sent
    
  def getSentiment(self):
    return self.sentiment
    
  def getLemma(self): 
      return self.lemma
    
  def setLemma(self,lemma):
      self.lemma = lemma
    
  def getPos(self):
      return self.pos
    
  def setPos(self,pos):
      self.pos = pos
      
  def getId(self):
      return self.tid
      
  def setId(self,id):
      self.tid = id

  def getShortPos(self):
    if self.pos==None:
      return None
    auxpos=self.pos.lower()[0]
    if auxpos == 'g': auxpos='a'
    elif auxpos == 'a': auxpos='r'
    return auxpos
    
  def __str__(self):
    if self.tid and self.lemma and self.pos:
        return self.tid+'\n\t'+self.lemma.encode('utf-8')+'\n\t'+self.pos
    else:
        return 'None'
      
    
    
    
    