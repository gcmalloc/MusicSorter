import os
import sys
import argparse
import threading
import re
import magic

import musicfile


"""
Directory walker, handle the creation of the musicfile classes instances
"""


class MusicWalker(threading.Thread):

    """
    Integer, correspond to the number of file already read
    """
    music_file_count = 0

    """
    Initialisation of the magic file library
    """
    magic = magic.Magic()

    """
    dictionnary that establish a correspondance between mime type and
    music type file, as handled by the musicfile module
    """
    MUSIC_TYPES = {'audio/mpeg': 'mp3', 'audio/flac': 'flac'}

    """
    Default initialisation
    """
    def __init__(self, path, args):
        threading.Thread.__init__(self)
        self.path = path
        self.args = args

    """
    launch the walker, create MusicFile instance accoring to their type
    then handle
    """
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
                    #sanitize the file's tag according to the parameters stored
                    #in flag
                    if music_file:
                        if args.flag_print:
                            print music_file
                        if args.flag_capital:
                            music_file.capitalize_all()
                        if args.flag_move():
                            music_file.move_with_condition()
                        if arg.flag_brainz:
                            music_file.sanitize_with_musicBrainz()
                        if arg.flag_brainz_force:
                            music_file.guess_musicbrainz()
                        if arg.flag_audio_guess:
                            music_file.guess_sound()
                        if args.flag_move:
                            fil.move_with_condition(args)

    """
    extract the type of a file according to the music file notation
    @param the absolute path of the music file
    @return  None if the file is not a recognised music file
                the music file type according to the music type notation
    """
    @staticmethod
    def get_music_type(music_file):
        music_type = get_type(music_file)
        if music_type:
            return music_type
        else:
            return None

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
        self.dir = args.dir
        self.flag_count = args.c
        self.flag_print = args.p
        self.flag_capital = args.C
        self.flag_brainz = args.b
        self.flag_brainz_force = args.B
        self.flag_audio_guess = args.a
        #TODO
        self.flag_move = False
        self.match = self.replace_match(args.m[0])

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
    metavar="dir", type=str, help="The location of the directories")
    args = parser.parse_args(["-m", "title,album", "/home/malik/Public"])
    clean_params = Params(args)
    MusicWalker(clean_params.dir, clean_params).start()

main()
