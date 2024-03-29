import os
import argparse
import threading
import sys
import logging

from musicfile import MusicFile
from musicfile import NotAMusicFileException
from musicfilecluster import MusicFileCluster

"""
Directory walker, handle the creation of the musicfile classes instances
"""


class MusicWalker(threading.Thread):

    """
    Default initialisation
    """
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.directories = args.directories
        self.args = args
        self.music_file_count = 0

    """
    Launch the walker, create MusicFile instance accoring to their type
    then handle
    """
    def run(self):
        print("Music Sorter is launched")
        for directory in self.directories:
            for e in os.walk(directory, self.dir_parser):
                self.dir_parser(*e, base_dir=directory)

    """
    Parse the directory with the given parameter
    """
    def dir_parser(self, dirpath, dirnames, filenames, base_dir):
        #we create a cluster from the directory
        cluster = MusicFileCluster(os.path.relpath(dirpath, base_dir))
        for f in filenames:
            logging.debug(f)
            abs_file_path = os.path.join(dirpath, f)
            try:
                music_file = MusicFile(abs_file_path)
                cluster.add(music_file)
            except NotAMusicFileException:
                logging.info("%s is not a music file" % abs_file_path)
                continue
            except IOError as e:
                logging.info(e)
                continue

            #sanitize the file's tag according to the parameters stored
            #in flag
            if music_file:
                #General stats
                if self.args.flag_count:
                    self.music_file_count += 1
                if self.args.flag_print:
                    print(music_file)

                #guess
                if self.args.flag_path_guess:
                    music_file.guess_path()
                if self.args.flag_audio_guess:
                    music_file.guess_sound()

                #Sanitizing
                if self.args.flag_capital:
                    music_file.capitalize_tag()
                if self.args.flag_brainz:
                    music_file.sanitize_with_musicBrainz()

        #clustering
        logging.debug(cluster)
        if self.args.flag_cdid:
            cluster.guess_with_cdid()
        if self.args.flag_path_guess:
            cluster.guess_from_directory()

        for f in filenames:
            #write the tag for good
            logging.debug("Will write the following tags :")
            logging.debug(f)
            if not self.args.flag_soft:
                music_file.save()

            #MOVING
            if self.args.path:
                music_file.move(self.args.path)

    """
    Parse the directory, try to guess the name of every tag it can find
    """
    def dir_parser_auto(self, dirpath, dirnames, filenames, base_dir):
        #at first create an empty cluster
    cluster = MusicFileCluster(os.path.relpath(dirpath, base_dir))
    #find all the music file in the directory
    for file_path in filenames:
        abs_file_path = os.path.join(dirpath, file_path)
        try:
            music_file = MusicFile(abs_file_path)
        except NotAMusicFileException:
            #just ignore this file
            logging.debug("File {} was not detected as a music file".format(file_path))
            continue


        #do we have enough right tag to go on from here  ?
        if cluster.contains_empty_tag;

        else:
        #at first we gonna try the cddb batch search
)


"""
Flag handler, rename the flag, create the matching pattern for the music
file tags
"""


class Params():

    """
    init function
    @param an instance of the ArgumentParser class
    """
    def __init__(self, args):
        self.directories = args.directories
        self.flag_count = args.c
        self.flag_print = args.p
        self.flag_capital = args.C
        self.flag_brainz = args.b
        self.flag_brainz_force = args.B
        self.flag_audio_guess = args.a
        self.flag_path_guess = args.P
        self.flag_cdid = args.D
        self.flag_soft = args.s
        if args.m:
            self.path = args.path
        else:
            self.path = None
        #self.match = self.replace_match(args.m[0])
        if args.d == True:
            self.toggle_debug_mode()

    """
    toggle the debug mode
    """
    def toggle_debug_mode(self):
        logging.basicConfig(level=logging.DEBUG)
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
    parser.add_argument('-P', action="store_true", default=False, \
    help="Use the path of the file to try to guess non existing tags")
    parser.add_argument('-C', action="store_true", default=False, \
    help="Capitalize each word in all the tags")
    parser.add_argument('-D', action="store_true", default=False, \
    help="Use CDDB database and discid to guess non existing tags")
    parser.add_argument('-b', action="store_true", default=False, \
    help="Use music Brainz database to correct existing tags")
    parser.add_argument('-B', action="store_true", default=False, \
    help="Use music Brainz database to try to guess non existing tags")
    parser.add_argument('-a', action="store_true", default=False, \
    help="Use the audio print of file to guess the uncomplete tag")
    parser.add_argument('-m', action="store", metavar="path", \
    type=str, nargs=1, help="move the music file to the predifined path\
    which use format ")
    parser.add_argument('-s', action="store_true", default=False, \
    help="Toggle soft mode, don't do any actual changes")
    parser.add_argument('-d', action="store_true", default=False, \
    help="Toggle debug mode")
    #parser.add_argument('-s', metavar="location", \
    #help="Move the music file according to the list argument, each \
    #argument which will be replaced is of this form :{element}")
    parser.add_argument('directories', nargs='+', action="store", \
    metavar="directory", type=str, help="The location of the directories")
    args = parser.parse_args(sys.argv[1:])
    clean_params = Params(args)
    t = MusicWalker(clean_params)
    t.run()


#MusicWalker(sys.argv[1], None).run()
main()
