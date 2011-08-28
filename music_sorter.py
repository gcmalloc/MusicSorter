import os
from mutagen.mp3 import MP3
import sys
import argparse

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

   def pprint(self, maxsize=100):
      for k in self.audio.keys():
         if len(str(self.audio[k])) < maxsize:
            sys.stdout.write("   " + k + ":")
            print self.audio[k]


def invert(dict):
   reversed = dict([(v,k) for (k,v) in dict])
   return reversed

def call(path):
   dir = os.listdir(path)
   mp3files = filter(lambda x: x.endswith("mp3"), dir)
   for i in mp3files:
      fil = MusicFile(path + "/" +i)
      if not fil.has_key('title'):
         print "|"
   for i in dir:
      if os.path.isdir(path+"/"+i):
         call(path+"/"+i)

def main():
   parser = argparse.ArgumentParser(description='Sort Music according to id3 tags')
   parser.add_argument('-c', action="store_true", default=False, help="Count the number of Music files that match the descriptor")
   parser.add_argument('-p', action="store_true", default=False, help="print the path of all the file matching the paramerers")
   parser.add_argument('-m', action="store", metavar="conditions", type=str, nargs=1, help="File descriptor, ban be list of matching argument separeted by & and |, for respectively and and or. the arguments are in the list of argument")
   parser.add_argument('-s', metavar="location", type=str, help="move the music file according to the list argument, each argument which will be replaced is of this form :{element}")
   parser.add_argument('directories', nargs='+', action="store", metavar="dir", type=str, help="The location of the directories")
   args = parser.parse_args("-c /home/malik/Public")
   print args
   dir = "/home/malik/Public"
   call(dir)

main()
