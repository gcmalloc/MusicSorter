import logging
import re, urllib
import eyeD3
import os
try:
    import lastfm
    last_fm_support = True
except ImportError:
    last_fm_support = False
    
def need_last_fm_support(f):
    def wrapper(*args, **kwargs):
        if last_fm_support:
            f()
        else:
            logging.error("no last fm support")
    return wrapper

"""
Implementation of a MusicFileCluster. This is a representation of music
that belong to the same directory. This permit to take in consideration
their proximity in the directory tree
"""


class MusicFileCluster(object):

    """
    Constructor that take the absolute dirname and a number of musicFile.
    """
    def __init__(self, abs_dirname, *musicFile):
        self.musicFiles = list()
        for i in musicFile:
            self.musicFile.append(i)
        self.abs_dirname = abs_dirname
        self.total_time = 0
        self.total_frames = ''

    def add(self, musicFile):
        self.musicFiles.append(musicFile)
        
    def __str__(self):
        return "Cluster is { \n" + "\n    ".join([str(mus.path) for mus in self.musicFiles]) + "\n}"
    
    def compute_discid(self):
            n = 0
            self.num_files = len(self.musicFiles)
            sorted_musicFiles = sorted(self.musicFiles, key=lambda k:k.path)
            for f in sorted_musicFiles:
                playTime = f.length()
                self.total_frames = self.total_frames + str(self.total_time * 75) + " "
                self.total_time += playTime
                n += MusicFileCluster.cddb_sum(playTime)
            tmp = ((long(n) % 0xFF) << 24 | self.total_time << 8 | self.num_files)
            self.disc_id = '%08lx' % tmp
    
    
    @staticmethod
    def cddb_sum(n):
        ret = 0
        while n > 0:
            ret = ret + (n % 10)
            n = n / 10
        return ret

    def guess_with_cddb(self):
        if not self.disc_id:
            self.compute_discid()
        logging.debug("guessing cddb with id " + self.disc_id)
        self.search()

    def search(self):
        searchstring = self.disc_id + " " + str(self.num_files) + " " + self.total_frames + str(self.total_time)
        logging.debug("searching with {}".format(searchstring))
        logging.debug("total frames " + self.total_frames)
        searchstring = searchstring.replace(' ', '+')
        results = urllib.urlopen('http://freedb.freedb.org/~cddb/cddb.cgi?cmd=cddb+query+' + searchstring + '&hello=cddbsearch+localhost+xmcd+2.1&proto=6')
        tags = []
        for raw_line in results.readlines()[1:-1]:
            line = raw_line.split(' ')
            genre = line[0]
            cddbid = line[1]
            #title = line[2:].split("/")[0]
            title = ' '.join(line[2:]).split("/")
            artist = title[0].strip()
            track = title[1].strip()
            tags.append({'genre':genre, 'cddbid':cddbid, 'title':track, 'artist':artist})
        return tags

    def getResult(self, genre, cddbid):
        tracknames = []
        searchstring = genre + " " + cddbid
        searchstring = searchstring.replace(' ', '+')
        results = urllib.urlopen('http://freedb.freedb.org/~cddb/cddb.cgi?cmd=cddb+read+' + searchstring + '&hello=cddbsearch+localhost+xmcd+2.1&proto=6')
        if results:
            for line in results:
                if re.match(r'^TTITLE',line):
                    trackname = re.sub(r'^TTITLE\d+=','',line)
                    tracknames.append(trackname.rstrip("\n"))
        return tracknames

    @need_last_fm_support
    def guess_from_name(self):
        clean_dirname = self.abs_dirname.strip(string.digits)
        #let's do a little search to see if we can find information 
        #based on the directory name
        
    
    def general_search(self, searchString):
        officialfm.album()
        return ''
