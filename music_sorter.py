import os
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import sys
import argparse
import threading
import magic
import re

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
            print self.audio[k]

   def __repr__(self):
      return self.__str_()

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

class MP3MusicFile(MusicFile):
   def __init__(self, path):
      MusicFile.__init__(self, path, MP3)

class FLACMusicFile(MusicFile):
   def __init__(self, path):
      MusicFile__init__(self, path, FLAC)

class MusicDir(threading.Thread):
   m = magic.Magic()
   MUSIC_TYPES = ['mp3']
    #lock for the directory all thread test
    #Lock()

   def __init__(self, path, args):
      threading.Thread.__init__(self)
      self.path = path
      self.args = args

   def run(self):
      dir_ls = os.listdir(self.path)
      for i in filter(MusicDir.filter_types, dir_ls):

            fil = MusicFile(path + "/" + i)#there is maybe a better way to do it
            if fil.condition_tester(args.m):
               return
            if args.p:
               print fil
            if args.m:
               fil.move_with_condition(args)
      for i in filter(os.path.is_dir, dir_ls):
            mus_dir = MusicDir(i)
            mus_dir.run()
      music_files = filter(filter_types, dir_ls)


   @staticmethod
   def filter_types(music_file):
      print m.from_file(music_file)
      return x.endswith("mp3")    #TODO real test of file type

class Params():
   MATCH_REGEX = '{([^{}]*)}'
   def __init__(self, args):
      self.c = args.c
      self.p = args.p
      self.m = self.replace_match(args.m[0])

   def replace_match(self, match):
      while re.search(self.MATCH_REGEX, match):
         match = re.sub(self.MATCH_REGEX, 'self.has_key(\'\\1\')', match)
      return match
def main():
   parser = argparse.ArgumentParser(description='Sort Music according to id3 tags')
   parser.add_argument('-c', action="store_true", default=False, help="Count the number of Music files that match the descriptor")
   parser.add_argument('-p', action="store_true", default=False, help="print the path of all the file matching the paramerers")
   parser.add_argument('-b', action="store_true", default=False, help="capitalize each word in the title")
   parser.add_argument('-m', action="store", metavar="conditions", type=str, nargs=1, help="File descriptor, ban be list of matching argument separeted by & and |, for respectively and and or. the arguments are in the list of argument")
   parser.add_argument('-s', metavar="location", help="move the music file according to the list argument, each argument which will be replaced is of this form :{element}")
   parser.add_argument('directories', nargs='+', action="store", metavar="dir", type=str, help="The location of the directories")
   args = parser.parse_args(["-m", "{title}&{album}", "/home/malik/Public"])
   print args
   Params(args)
   #dir = "/home/malik/Public"
   #MusicDir(dir, args).start()

main()
