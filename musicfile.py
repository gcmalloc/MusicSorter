from mutagen.mp3 import MP3
from mutagen.flac import FLAC

"""
super class for all the music file of all type
give the way to access in a simple fashion the tags
"""


class MusicFile():

    """
    Dictionnary to transform the standardised id3 tag to a more human
    readable tag, this dictionnary is also a list of tag we extract from
    the music file
    """
    USEFUL_TAG = {'TPE1': 'artist', 'TALB': 'album', 'TIT2': 'title',
                  'TRCK': 'track', 'TCOM': 'composer', 'TDAT': 'date',
                  'TYER': 'year'}

    """
    initialisation function
    @param path:
    @param function used to get the tags
    """
    def __init__(self, path):
        """
        absolute path to the path
        """
        self.path = path
        self.tags = dict()
        self.parse_tag()

    """
    init helper to extract the tags from the
    """
    def parse_tag(self):
        for k in self.USEFUL_TAG:
            v = self.USEFUL_TAG[k]
            #we consider the tag none existant if the value is empty
            if v != "":
                try:
                    self.tags[v] = self.audio[k]
                except KeyError:
                    pass

    #sanitize method, clean the tag using the following technique
    #just idea for the moment

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
    test if the music file contain a key
    """
    def has_tag(self, tag):
        return key in self.tags

    """
     print all tags that mutagen can find
     @param maximum length of all the content
    """
    def __str__(self, maxsize=100):
        for k in self.audio.keys():
            if len(str(self.audio[k])) < maxsize:
                sys.stdout.write("  " + k + ":")
                print self.audio[k]

    """
    @return the path if the condition for the existence of the tags
            are fullfilled
            None otherwise
    """
    def move_with_condition(self, condition, new_place):
        #test if all tags are defined for this element
        if filter(lambda x, y: x and y,  self., True):
            #move the file
            new_path = new_place
            os.move(path, newpath)
        else:
            #keep it there  
            
    """
    Create the new folder if needed, return the 
    """

#Subclasses which handle the multiple format

"""
Subclass of MusicFile for MP3 only
"""


class Mp3File(MusicFile):

    """
    Constructor for the mp3 file
    """
    def __init__(self, path):
        self.audio = MP3(path)
        MusicFile.__init__(self, path)

"""
Subclass of MusicFile for FLAC only
"""


class FlacFile(MusicFile):

    """
    Constructor for the Flac file
    """
    def __init__(self, path):
        self.audio = FLAC(path)
        MusicFile.__init__(self, path)
