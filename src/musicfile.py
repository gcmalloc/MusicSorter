from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.flac import FLACNoHeaderError
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.mp3 import MP3
import mutagen
from urllib2 import HTTPError
from time import sleep

import string
import os
import errno
import logging
from musicbrainz2.webservice import Query, TrackFilter, WebServiceError
import acoustid

"""
The acoustid api key to access the database.
"""

ACOUSTID_KEY = "jwsxE9b6"


"""
Define the main tags the musicFile must find to consider the file as done
"""

OBLIGATORY_TAG =['title', 'artist', 'album']

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
    @param the absolute path of the file
    @raise A NotAMusicFileException if the file cannot be read as a musicFile
    """

    def __init__(self, path):
        try:
            logging.debug("Trying mp3")
            self.tags = MP3(path, ID3=EasyID3)
            #self.tags = EasyID3(path)
        except mutagen.mp3.HeaderNotFoundError:
            try:
                logging.debug("Trying flac")
                self.tags = FLAC(path)
            except FLACNoHeaderError:
                try:
                    logging.debug("Trying general")
                    self.tags = EasyID3(path)
                except ID3NoHeaderError:
                    raise NotAMusicFileException
        self.path = path

    """
    sanitize method, clean the tag using the following technique
    just idea for the moment
    """
    def sanitize_with_musicBrainz(self):
        titleName = self['title']
        artistName = self['artist']
        albumName = self['album']
        q = Query()
        try:
            logging.debug("Querying with title:{},artist:{},album:{}"
            .format(titleName, artistName, albumName))
            f = TrackFilter(title=titleName, artistName=artistName,
            releaseTitle=albumName, limit=2)
            results = q.getTracks(f)
            logging.debug("results are " + str(results))
        except WebServiceError as e:
            logging.error("Failed to contact musicbrainz server.")
            if str(e)[:15]=="HTTP Error 503:":
                logging.info("Pausing for a moment, \
                the musicbrainz server doesn't handle too much request")
                sleep(60)
            return self.sanitize_with_musicBrainz()
        self.treat_musicbrainz_result(results)

    """
    A simple way to sort the results obtain by a query to the musicbrainz
    database and put them into the correct tag
    @return True if the results can be put into the corresponding tag
            False otherwise
    """
    def treat_musicbrainz_result(self, results):
        if len(results) == 0:
            logging.debug("No result found")
            return False
        for result in results:
            logging.debug("A result was found")
            if result.score == 100:
                track = result.track
                logging.debug("A perfect match seems to be found !!")
                possible_releases = track.getReleases()
                if len(possible_releases) != 1:
                    logging.debug("Multiple album, I will try to guess")
                    for rel in possible_releases:
                        print(dir(rel))
                        exit(0)
                    return False
                else:
                    release = possible_releases[0]
                logging.debug(dir(track))
                logging.debug("tags are :" + str(track.getTags()))
                dir(track)
                self['title'] = track.title
                self['artist'] = track.artist.name
                self['album'] = release.getTitle()
                #self.tags['album'] =
                return

    """
    guess the title from the sound using the sound fingerprint
    using acoustID api
    """
    def guess_sound(self):
        if 'title' in self and 'artist' in self:
            logging.debug("We already have title and artist for this one")
            return
        logging.debug(self.path)
        logging.debug(ACOUSTID_KEY)
        try:
            match = acoustid.match(ACOUSTID_KEY, self.path)
        except:
            return
        for score, recording_id, title, artist in match:
            if score > 0.99:
                #we are quite sure this result match
                logging.debug("Match Found score:%s, title:%s, artist:%s",
                score, title, artist)
                self['title'] = title
                self['artist'] = artist
            else:
                #the result are not sure enough
                logging.debug("The result doesn't seems sure enough.")

    """
    guess the tags from the path
    """
    def guess_path(self):
        if self['artist'] and self['album'] and self['title']:
            logging.debug("Cannot guess any further with only the title")
            return
        #let's try to find album name or artist name from the path, if it's
        #not already set
        clean_path = path_split(self.path)
        logging.debug("Trying to guess on %s" % str(clean_path))
        logging.debug("Clean title:%s" % clean_title(clean_path[-1]))
        #try to guess the album if not already set
        if not self['title']:  # Our worst case
            #we remove all trailing number, trailing '-'
            #and the extension and try to find it in our database
            possible_title = clean_path[-1]
            logging.debug("Title could be {}".format(possible_title))

    """
    get the tag, the name of the tag must be in the value of USEFUL_TAG
    @param the name of the tag
    @return the value of the tag
    """
    def __getitem__(self, key):
        try:
            #return the first item as default
            tag = self.tags[key]
        except KeyError:
            return None
        if not tag:  # if tag is empty
            return None
        else:
            return tag[0]

    """
    set the tag, the name of the tag must be in the value of USEFUL_TAG
    @param the key of the tag
    the new value of the tag
    """
    def __setitem__(self, key, value):
        #set the tag without writing them
        self.tags[key] = str(value)

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
            ret += ["\t %s:%s" % (k, self[k])]
        return "\n".join(ret)

    """
    move this music file in the good place
    """
    def move(self, new_basedir, path_format):
        formatted_path = path_format.format(**self.tags)
        new_dir = os.join(new_basedir, formatted_path)
        try:
            mkdir_p(new_dir)
        except OSError:
            logging.info("Directory %s already exist" % new_dir)
        #extract the extension
        try:
            ext = self.get_extension()
        except:  # TODO specify error
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
    Get the length of the track in milisecond
    """
    def length(self):
        return int(self.tags.info.length)

    """
    Get the bitrate of the track
    """
    def bitrate(self):
        return int(self.tags.info.bitrate)

    """
    """
    def has_mandatory_tag(self):
        for tag in OBLIGATORY_TAG:
            if tag not in self:
                return False
        return True
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

"""
A little test for path cleaning to extract information from the path of
the music file
    Artist

    Album

    Listitem

    Track No

    Characters to separate the fields

    File Type (e.g.mp3)
"""


def path_split(path, depth=3):
    split_path = []
    for i in range(depth + 1):
        path = os.path.split(path)
        split_path = [path[1].replace("_", " ")] + split_path
        path = path[0]
    return split_path[1:]

"""
clean a title
"""


def clean_title(title):
    pass
    #return os.path.splitext(title)[0].strip(string.digits + '- ')
