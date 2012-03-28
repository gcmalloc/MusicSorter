from mutagen.easyid3 import EasyID3 as ID3
from mutagen.id3 import ID3NoHeaderError

import string
import os
import errno
import logging

class NotAMusicFileException(Exception):
    pass

"""
super class for all the music file of all type
give the way to access in a simple fashion the tags
"""

class MusicFile():

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
        pass

    def guess_musicbrainz(self):
        pass

    """
    guess the title from the sound using a sound
    """
    def guess_sound(self):
        pass

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
        
    """
    def move(self, new_basedir, path_format):
        formatted_path = path_format.format(self.tags)
        new_dir = os.join(new_basedir, formatted_path)
        try:
            mkdir_p(new_basedir)
        except OSError:
            logging.info("Directory %s already exist" % new_dir)
        #extract the extension
        try:
            ext = self.get_extension()
        except:#TODO specify
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
        return os.path.splitext(path)[-1]

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

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e: # Python >2.5
        if e.errno == errno.EEXIST:
            pass
        else: 
            raise
