import os
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import sys
import argparse
import threading
import magic
import re

class MusicWalker(threading.Thread):

   m = magic.Magic()
   MUSIC_TYPES = {'audio/mpeg','mp3','audio/flac':'flac'}
   #lock for the directory all thread test
   #Lock()

   def __init__(self, path, args):
      threading.Thread.__init__(self)
      self.path = path
      self.args = args

   def run(self):
      dir_ls = os.listdir(self.path)
      for i in filter(MusicWalker.filter_types, dir_ls):
            music_file = MusicFile(os.path.join(path, i))
            if fil.condition_tester(args.m):
               return
            if args.p:
               print fil
            if args.m:
               fil.move_with_condition(args)
      for i in filter(os.path.is_dir, dir_ls):
            mus_dir = MusicDir(i)
            mus_dir.run()
      music_files = map(filter_types, dir_ls)
   
   @staticmethod
   def filter_types(music_file):     
      if get_type()
   
   @staticmethod
   def get_type(music_file):
      mime_type = magic.from_file(music_file, mime=True)
      try:
         music_type = self.MUSIC_TYPES[mime_type]
         return music_type
      except:
         return None

class Params():
   MATCH_REGEX = '{([^{}]*)}'
   def __init__(self, args):
      self.flag_count = args.c
      self.flag_print = args.p
      self.flag_capi = args.b
      self.match = self.replace_match(args.m[0])

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
   dir = "/home/malik/Public"
   MusicDir(dir, args).start()

main()
