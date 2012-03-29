from mutagen.easyid3 import EasyID3 as ID3
from mutagen.id3 import ID3NoHeaderError

import string
import os
import errno
import logging
from musicbrainz2.webservice import Query, TrackFilter, WebServiceError

"""
Exception launched if the music file is not a id3v2 tag
"""


class NotAMusicFileException(Exception):
    pass

"""
super class for all the music file of all type
give the way to access in a simple fashion the tags
"""


class MusicFile(object):

    """
    initialisation function
    @param path:
    @param function used to get the tags
    """
    def __init__(self, path):
        """
        absolute path to the path
        """
        try:
            self.tags = ID3(path)
        except ID3NoHeaderError:
            raise NotAMusicFileException
        self.path = path

    """
    sanitize method, clean the tag using the following technique
    just idea for the moment
    """
    def sanitize_with_musicBrainz(self):
        titleName = self.tags['title'][0]
        artistName = self.tags['artist'][0]
        albumName = self.tags['album'][0]
        q = Query()
        try:
            logging.debug(titleName)
            logging.debug(artistName)
            f = TrackFilter(title=titleName, artistName=artistName,
            releaseTitle=albumName)
            results = q.getTracks(f)
        except WebServiceError as e:
            logging.debug(e)
            logging.error("Failed to contact musicbrainz server.")
            return
        if len(results) == 0:
            logging.debug("No result found")
            return

        for result in results:
            logging.debug("A result was found")
            if result.score == 100:
                track = result.track
                logging.debug("A perfect match seems to be found !!")
                possible_releases = track.getReleases()
                if len(possible_releases) != 1:
                    logging.debug("Multiple album, I will try to guess")
                    #TODO
                    return
                else:
                    release = possible_releases[0].getTitle()
                self.tags['title'] = track.title
                self.tags['artist'] = track.artist.name
                self.tags['album'] = release
                return

    """
    guess the non existing tag with musicBrainz
    """
    def guess_musicbrainz(self):
        pass

    """
    guess the title from the sound using a sound
    """
    def guess_sound(self):
        pass

    """
    guess the tags from the path
    """
    def guess_path(self):
        splitted_path = os.path.dirname(self.path)

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
        #write down the tags directly with mutagen

    def keys(self):
        return self.tags.keys()

    """
    test if the music file contain a certain tag
    """
    def has_key(self, tag):
        return tag in self.tags

    """
     print all tags that mutagen can find
     @param maximum length of all the content
    """
    def __str__(self, maxsize=100):
        ret = [self.path]
        for k in self.tags.keys():
            ret += ["\t %s:%s" % (k, self.tags[k])]
        return "\n".join(ret)

    """
    @return the path if the condition for the existence of the tags
            are fullfilled
            None otherwise
    """
    def move_with_condition(self, condition, new_basedir, path_format):
        #test if all tags are defined for this element
        if condition:
            self.move(new_basedir, path_format)

    """
    move this music file in the good place
    """
    def move(self, new_basedir, path_format):
        formatted_path = path_format.format(self.tags)
        new_dir = os.join(new_basedir, formatted_path)
        try:
            mkdir_p(new_dir)
        except OSError:
            logging.info("Directory %s already exist" % new_dir)
        #extract the extension
        try:
            ext = self.get_extension()
        except:  # TODO specify
            logging.error("Moving file %s failed, extension is undefined"
            % self.path)
            return
        formatted_path = path_format.format(self.tags)
        new_filename = os.path.join(new_basedir, formatted_path + ext)
        try:
            os.mv(self.path, new_filename)
        except OSError:
            logging.error("Moving file %s failed, cannot move the file")

    """
    return the extension of this file according to it's name
    it can be not accurate if the extention doesn't correspond to
    the real file type.
    """
    def get_extension(self):
        return os.path.splitext(self.path)[-1]

    """
        capitalize all tag by default or a list of specific tag
    """
    def capitalize_tag(self, tag=None):
        for tag in self.tags:
            self.tags[tag] = [string.capwords(i) for i in self.tags[tag]]

    """
    save modification to the id3 tag
    """
    def save(self):
        self.tags.save()

"""
Emulate the mkdir -p command, create a directory and all it's children
"""


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:  # Python >2.5
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
