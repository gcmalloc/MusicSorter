from mutagen.mp3 import MP3
from mutagen.flac import FLAC

"""
super class for all the music file of all type
give the way to access in a simple fashion the tags
"""
class MusicFile():
   """
   dictionnary to transform the standardised id3 tag to a more human 
   readable tag, this dictionnary is also a list of tag we extract from 
   the music file
   """
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
      self.parse_tag()
      
   """
   init helper to extract the tags from the  
   """
   def parse_tag():
      for k in self.USEFUL_TAG:
         v = self.USEFUL_TAG[k]
         #we consider the tag none existant if the value is empty
         if v != "":
            try:
               self.tags[v] = self.audio[k]
            except KeyError:
               pass
               
   #sanitize method, clean the tag using the following technique
   #just idea for the moment
   
   def sanitize_with_musicBrainz(self):
      pass

   def guess_musicbrainz(self):
      pass
   
   """
   guess the title from the sound using 
   """
   def guess_sound(self):
      pass
   
   #end of sanitizing methods
   """
   get the tag, the name of the tag must be in the value of USEFUL_TAG
   @param the name of the tag
   @return the value of the tag
   """
   def __getitem__(self, key):
      return self.tags[key]

   """
   set the tag, the name of the tag must be in the value of USEFUL_TAG
   @param the key of the tag
          the new value of the tag  
   """
   def __setitem__(self, key, value):
      self.tags[key] = str(value)

   def keys(self):
         return self.tags.keys()

   """
   test if the music file contain a key
   """
   def has_key(self, key):
      return self.tags.has_key(key)
   
   """
    print all tags that mutagen can find
    @param maximum length of all the content
   """
   def __str__(self, maxsize=100):
      for k in self.audio.keys():
         if len(str(self.audio[k])) < maxsize:
            sys.stdout.write("   " + k + ":")
            print self.audio[k]=

   """
    @return the path if the condition for the existence of the tags are fullfilled
            None otherwise
   """
   def move_with_condition(self):
      if condition_tester():
            return path.substitue#syntax
      else:
         return none
   
   """
   test if the file match the matching params on the tags
   a way to test the presence of tags in the method
   """
   def condition_tester(self, matching):
      pass
   
