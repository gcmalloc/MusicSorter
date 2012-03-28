import os
import argparse
import threading
import sys
import logging

from musicfile import MusicFile
from musicfile import NotAMusicFileException

"""
Directory walker, handle the creation of the musicfile classes instances
"""

class MusicWalker(threading.Thread):

    """
    Integer, correspond to the number of file already read
    """
    music_file_count = 0

    """
    Default initialisation
    """
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.directories = args.directories
        self.args = args

    """
    launch the walker, create MusicFile instance accoring to their type
    then handle
    """
    def run(self):
        print "launch"
        for directory in self.directories:
            for e in os.walk(directory, self.dir_parser):
                self.dir_parser(*e)
    
    """
    parse the directory
    """
    def dir_parser(self, dirpath, dirnames, filenames):
        for f in filenames:
            abs_file_path = os.path.join(dirpath, f)
            try:
                music_file = MusicFile(abs_file_path)
            except NotAMusicFileException:
                logging.info("%s is not a music file" % abs_file_path)
                continue
            #sanitize the file's tag according to the parameters stored
            #in flag
            if music_file:
                if self.args.flag_print:
                    print(music_file)
                if self.args.flag_capital:
                    music_file.capitalize_tag()
                if self.args.flag_move:
                    music_file.move_with_condition()
                if self.args.flag_brainz:
                    music_file.sanitize_with_musicBrainz()
                if self.args.flag_brainz_force:
                    music_file.guess_musicbrainz()
                if self.args.flag_audio_guess:
                    music_file.guess_sound()
                if self.args.flag_move:
                    fil.move_with_condition(self.args)

    """
    Wrapper around the magic module to handle audio file only.
    @param the absolute path to the file we want to analyse
    @return None if the mime_type s not in the MUSIC_TYPES dict.
    """
    @staticmethod
    def get_type(music_file):
        mime_type = self.magic.from_file(music_file, mime=True)
        music_type = self.MUSIC_TYPES.get(mime_type)
        return music_type

"""
Flag handler, rename the flag, create the matching pattern for the music
file tags
"""


class Params():

    """
    Separator for the match
    """
    MATCH_SEPARATOR = ","

    """
    init function
    @param an instance of the ArgumentParser class
    """
    def __init__(self, args):
        print(args)
        self.directories = args.directories
        self.flag_count = args.c
        self.flag_print = args.p
        self.flag_capital = args.C
        self.flag_brainz = args.b
        self.flag_brainz_force = args.B
        self.flag_audio_guess = args.a
        #TODO
        self.flag_move = False
        #self.match = self.replace_match(args.m[0])

    """
    replace to match to a python expression
    Not safe for now
    @return an array of tag that must be in the expression
    """
    def replace_match(self, match):
        matching_values = match.split(Params.MATCH_SEPARATOR)
        #ignore trailing spaces
        matching_values = [i.strip() for i in matching_values]
        return match

"""
main
handle the parsing of the argument and the first call to MusicWalker
"""


def main():
    parser = argparse.ArgumentParser(description='Sort Music according \
    to id3 tags')
    parser.add_argument('-c', action="store_true", default=False, \
    help="Count the number of Music files that match the descriptor")
    parser.add_argument('-p', action="store_true", default=False, \
    help="Print the path of all the file matching the paramerers")
    parser.add_argument('-C', action="store_true", default=False, \
    help="Capitalize each word in all the tags")
    parser.add_argument('-b', action="store_true", default=False, \
    help="Use music Brainz database to correct existing tags")
    parser.add_argument('-B', action="store_true", default=False, \
    help="Use music Brainz database to try to guess non existing tags")
    parser.add_argument('-a', action="store_true", default=False, \
    help="Use the audio print of file to guess the uncomplete tag")
    parser.add_argument('-m', action="store", metavar="conditions", \
    type=str, nargs=1, help="File descriptor, ban be list of matching \
    argument separeted by & and |, for respectively and and or. the \
    arguments are in the list of argument")
    #parser.add_argument('-s', metavar="location", \
    #help="Move the music file according to the list argument, each \
    #argument which will be replaced is of this form :{element}")
    parser.add_argument('directories', nargs='+', action="store", \
    metavar="directory", type=str, help="The location of the directories")
    args = parser.parse_args(sys.argv[1:])
    clean_params = Params(args)
    t = MusicWalker(clean_params)
    t.start()
    t.join()
    

#MusicWalker(sys.argv[1], None).run()
main()
