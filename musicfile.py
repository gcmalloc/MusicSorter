class MusicFile():
   USEFUL_TAG = {'TPE1':'artist', 'TALB':'album', 'TIT2':'title',
                 'TRCK':'track', 'TCOM':'composer','TDAT':'date',
                  'TYER':'year'}

   def __init__(self, path, open_function):
      self.path = path
      try:
         self.audio = open_function(path)
      except:
         self = None
         return
      self.tags = dict()

   def parse_tag():
      for k in self.USEFUL_TAG:
         v = self.USEFUL_TAG[k]
         #we consider the tag none existant if the value is empty
         if v != "":
            try:
               self.tags[v] = self.audio[k]
            except KeyError:
               pass

   def sanitize_with_musicBrainz(self):
      pass

   def guess_on_title(self):
      pass

   def guess_on_sound(self):
      pass

   def __getitem__(self, key):
      return self.tags[key]

   def __setitem__(self, key, value):
      self.tags[key] = str(value)

   def keys(self):
         return self.tags.keys()

   def has_key(self, key):
      return self.tags.has_key(key)

    #print all tags that mutagen can find
   def __str__(self, maxsize=100):
      for k in self.audio.keys():
         if len(str(self.audio[k])) < maxsize:
            sys.stdout.write("   " + k + ":")
            print self.audio[k]=

    #return the path if the condition for the existence of the tags are fullfilled
    #return None otherwise
   def move_with_condition(self, condition):
      if condition_tester():
            return path.substitue#syntax
      else:
         return none

   def condition_tester(self, matching):
      #matching = self.substitute_values(matching)
      #replace all occurence of things {} by self.has_key('string')
      pass
   def substitute_values(self, string):
      return string
