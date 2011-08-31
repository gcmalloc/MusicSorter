import os
from mutagen.mp3 import MP3
import sys
import argparse
import threading 

class MusicFile():
   USEFUL_TAG = {'TPE1':'artist','TALB':'album','TIT2':'title','TRCK':'track'}

   def __init__(self, path):
      self.path = path
      self.tags = dict()
      try:
         self.audio = MP3(path)
      except:
         return
      for k in self.USEFUL_TAG:
         v = self.USEFUL_TAG[k]
         try:
            self.tags[v] = self.audio[k]
         except KeyError:
            pass

   def __getitem__(self, key):
      return self.tags[key]

   def keys(self):
         return self.tags.keys()

   def has_key(self, key):
      return self.tags.has_key(key)

   def __str__(self, maxsize=100):
      for k in self.audio.keys():
         if len(str(self.audio[k])) < maxsize:
            sys.stdout.write("   " + k + ":")
            print self.audio[k]
    
    def _repr__(self):
        return self.__str_()
    
    def move_with_condition(self, condition):
        if condition:
    
    def condition_parser(self):
        
        
class MusicDir(threading.Thread):
    MUSIC_TYPES = ['mp3']
    #lock for the directory test 
    
    def __init__(self, path, args):
        threading.Thread.__init__(self)
        self.path = path
        self.args = args
    
    def run(self):
        dir_ls = os.listdir(self.path)
        for i in filter(MusicDir.filter_types, dir_ls):
            fil = MusicFile(path + "/" + i)#there is maybe a better way to do it
            if args.p:
                print fil
            else:
                fil.move_with_condition
        for i in filter(os.path.is_dir, dir_ls):
            mus_dir = MusicDir()
            mus_dir.run()
        music_files = filter(filter_types, dir_ls)#TODO real test of file type
        
    
    @staticmethod
    def filter_types(music_file):
        return x.endswith("mp3")    #TODO real test of file type
        
def main():
   parser = argparse.ArgumentParser(description='Sort Music according to id3 tags')
   parser.add_argument('-c', action="store_true", default=False, help="Count the number of Music files that match the descriptor")
   parser.add_argument('-p', action="store_true", default=False, help="print the path of all the file matching the paramerers")
   parser.add_argument('-m', action="store", metavar="conditions", type=str, nargs=1, help="File descriptor, ban be list of matching argument separeted by & and |, for respectively and and or. the arguments are in the list of argument")
   parser.add_argument('-s', metavar="location", type=str, help="move the music file according to the list argument, each argument which will be replaced is of this form :{element}")
   parser.add_argument('directories', nargs='+', action="store", metavar="dir", type=str, help="The location of the directories")
   args = parser.parse_args("-c /home/malik/Public")
   print args
   dir = "/home/malik/Music"
   MusicDir(dir, args).start()

main()
