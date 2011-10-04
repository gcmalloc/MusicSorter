import os
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
#from mutagen.ogg import OGG
import sys
import argparse
import threading
import magic
import re

class MusicFile():
    USEFUL_TAG = {'TPE1':'artist', 'TALB':'album', 'TIT2':'title',
                      'TRCK':'track', 'TCOM':'composer','TDAT':'date',
                        'TYER':'year'}
    
    def __init__(self, path):
        self.path = path
        self.tags = dict()

    def parse_tag():
        for k in self.USEFUL_TAG:
            v = self.USEFUL_TAG[k]
            #we consider the tag none existant if the value is empty
            if v != "":
                try:
                    self.tags[v] = self.audio[k]
                except:
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
        for k in self.audio.keys():
            if len(str(self.audio[k])) < maxsize:
                sys.stdout.write("  " + k + ":")
                print self.audio[k]

    def __repr__(self):
        return self.__str_()

     #return the path if the condition for the existence of the tags are fullfilled
     #return None otherwise
    def move_with_condition(self, condition, location):
        if condition_tester(self, condition ):
                return move #syntax
        else:
            return none

    def condition_tester(self, matching):
        #we just replace everypart
        #remove all spaces 
        #exec matching
        #matching = self.substitute_values(matching)
        #replace all occurence of things {} by self.has_key('string')
        return True
     
    def substitute_values(self, string):
        return string
    
    def move(self, ):
        pass
    
class MP3MusicFile(MusicFile):
    def __init__(self, path):
        MusicFile.__init__(self, path)
        self.audio = MP3(path)

class FLACMusicFile(MusicFile):
    def __init__(self, path):
        MusicFile.__init__(self, path)
        try:
            self.audio = FLAC(path)
        except:
            self = None
            return

#class OGGMusicFile(MusicFile):
    #def __init__(self, path):
        #MusicFile.__init__(self, path)
        #try:
            #self.audio = OGG(path)
        #except:
            #pass
            
class MusicDir(threading.Thread):
    m = magic.Magic()
    MUSIC_TYPES = ['mp3']
    args = None
     #lock for the directory all thread test
     #Lock()

    def __init__(self, path, args=None):
        if args:
            MusicDir.args = args
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        dir_ls = os.listdir(self.path)
        dir_ls = [os.path.join(self.path, i) for i in dir_ls]
        music_file_count = 0
        for i in filter(self.filter_types, dir_ls):
                music_file_count += 1
                fil = MP3MusicFile(i)#there is maybe a better way to do it
                if fil.condition_tester(MusicDir.args.m):
                    pass
                if MusicDir.args.p:
                    print fil
                if MusicDir.args.m:
                    fil.move_with_condition(args)
        for i in filter(os.path.isdir, dir_ls):
                mus_dir = MusicDir(i)
                music_file_count += mus_dir.run()
        return music_file_count

    def filter_types(self, music_file):
        if os.path.isfile(music_file):
            print magic.from_file(music_file)
        return music_file.endswith("mp3")     #TODO real test of file type

class Params():
    MATCH_REGEX = '{([^{}]*)}'
    def __init__(self, args):
        self.c = args.c
        self.p = args.p
        if args.m:
            self.m = self.replace_match(args.m[0])
        else:
            self.m = None
        

    def replace_match(self, match):
        while re.search(self.MATCH_REGEX, match):
            match = re.sub(self.MATCH_REGEX, 'self.has_key(\'\\1\')', match)
        return match
    
    def __repr__(self):
        return str(self.c) + " | " + str(self.p) + " | " + str(self.m)
    
def main():
    parser = argparse.ArgumentParser(description='Sort Music according to id3 tags')
    parser.add_argument('-c', action="store_true", default=False, help="Count the number of Music files that match the descriptor")
    parser.add_argument('-p', action="store_true", default=False, help="print the path of all the file matching the paramerers")
    parser.add_argument('-b', action="store_true", default=False, help="capitalize each word in the title")
    parser.add_argument('-m', action="store", metavar="conditions", type=str, nargs=1, help="File descriptor, ban be list of matching argument separeted by & and |, for respectively and and or. the arguments are in the list of argument")
    parser.add_argument('-s', metavar="location", help="move the music file according to the list argument, each argument which will be replaced is of this form :{element}")
    parser.add_argument('directories', nargs='+', action="store", metavar="dir", type=str, help="The location of the directories")
    args = parser.parse_args(["-p", "/home/malik/Music"])
    params = Params(args)
    dir = args.directories
    for i in dir:
        print MusicDir(i, params).run()

main()
