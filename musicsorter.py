import os
import sys
import argparse
import threading
import magic
import re

class MusicWalker(threading.Thread):
   music_file_count = 0
   m = magic.Magic()
   MUSIC_TYPES = {'audio/mpeg':'mp3','audio/flac':'flac'}
   #lock for the directory all thread test
   #Lock()

   def __init__(self, path, args):
      threading.Thread.__init__(self)
      self.path = path
      self.args = args

   def run(self):
      dir_ls = os.listdir(self.path)
      for element in dir_ls:
         if os.path.isdir(element):
            #recursive call
            music_dir = MusicWalker(i)
            music_dir.run()
         else:
            file_type = get_music_type()
            if file_type:
               music_file = MusicFile(os.path.join(self.path, i))
               if music_file:
                  if args.flag_print:
                     print music_file
                  if args.flag_capital:
                     music_file.capitalize_all()
                  if args.flag_move()
                     music_file.move_with_condition()
                  if arg.flag_brainz:
                     music_file.sanitize_with_musicBrainz()
                  if arg.flag_brainz_force:
                     music_file.guess_musicbrainz()
                  if arg.flag_audio_guess:
                     music_file.guess_sound()
                  if args.flag_move:
                     fil.move_with_condition(args)
      
   @staticmethod
   def get_music_type(music_file):     
      music_type = get_type(music_file)
      if music_type:
         return music_type
      else:
         return None
   
   @staticmethod
   def get_type(music_file):
      mime_type = magic.from_file(music_file, mime=True)
      music_type = self.MUSIC_TYPES.get(mime_type)
      return music_type

class Params():
   MATCH_REGEX = '{([^{}]*)}'
   def __init__(self, args):
      self.flag_count = args.c
      self.flag_print = args.p
      self.flag_capital = args.C
      self.flag_brainz = args.b
      self.flag_brainz_force = args.B
      self.flag_audio_guess = args.a
      #TODO
      self.flag_move = False
      self.match = self.replace_match(args.m[0])

   def replace_match(self, match):
      while re.search(self.MATCH_REGEX, match):
         match = re.sub(self.MATCH_REGEX, 'self.has_key(\'\\1\')', match)
      return match
      
def main():
   parser = argparse.ArgumentParser(description='Sort Music according to id3 tags')
   parser.add_argument('-c', action="store_true", default=False, help="Count the number of Music files that match the descriptor")
   parser.add_argument('-p', action="store_true", default=False, help="Print the path of all the file matching the paramerers")
   parser.add_argument('-C', action="store_true", default=False, help="Capitalize each word in all the tags")
   parser.add_argument('-b', action="store_true", default=False, help="Use music Brainz database to correct existing tags")
   parser.add_argument('-B', action="store_true", default=False, help="Use music Brainz database to try to guess non existing tags")
   parser.add_argument('-a', action="store_true", default=False, help="Use the audio print of file to guess the uncomplete tag")
   parser.add_argument('-m', action="store", metavar="conditions", type=str, nargs=1, help="File descriptor, ban be list of matching argument separeted by & and |, for respectively and and or. the arguments are in the list of argument")
   #parser.add_argument('-s', metavar="location", help="Move the music file according to the list argument, each argument which will be replaced is of this form :{element}")
   parser.add_argument('directories', nargs='+', action="store", metavar="dir", type=str, help="The location of the directories")
   args = parser.parse_args(["-m", "{title}&{album}", "/home/malik/Public"])
   print args
   Params(args)
   dir = "/home/malik/Public"
   MusicDir(dir, args).start()

main()
