import logging
import DiscID
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

    def add(self, musicFile):
        self.musicFiles.append(musicFile)
        
    def __str__(self):
        return "Cluster is { \n" + "\n    ".join([str(mus.path) for mus in self.musicFiles]) + "\n}"
        
    def weight_files():
        #files are together so they should look a bit the same
        pass

    def disc_idmp3(self):
        last = len(self.musicFiles)

        track_frames = []
        checksum = 0
        cdtime = 0
        
        adjust = 0
        
        for i, file in enumerate(self.musicFiles[:-1]):
            br = file.bitrate()#bitrate
            #pt = file.getPlayTimeString()#number o  time the music is playeds
            pt = "1"
            ms = file.length() * 1000#playtime in milisecond
            ms = ms + adjust#add ajust time for the  rest
            if i == 0:
                ms = 2000
            cdtime = cdtime + ms
            (min, sec, frame) = (cdtime / 60000, (cdtime%60000) / 1000, (((cdtime%60000)%1000)*75)/1000)
            #logging.debug('%02d:%02d.%02d  vbr=%d br=%d %s %s' %(min,sec,frame,br[0],br[1],pt,file))
            checksum = checksum + DiscID.cddb_sum(min*60 + sec)
            track_frames.append(min*60*75 + sec*75 + frame)

        audioFile = self.musicFiles[-1]
        ms = audioFile.length() * 1000
        ms = ms + adjust
        cdtime = cdtime + ms
        (min, sec, frame) = (cdtime/60000,(cdtime % 60000) / 1000, ((( cdtime % 60000) % 1000) * 75) / 1000)
        track_frames.append(min*60*75 + sec*75 + frame)

        total_time = (track_frames[-1] / 75) - (track_frames[0] / 75)
               
        discid = ((checksum % 0xff) << 24 | total_time << 8 | last)

        for i in range(0, last-1):
            secs = (track_frames[i+1] - track_frames[i])/75
            min = secs/60
            sec = secs%60
            print '%02d:%02d' %(min,sec)
        logging.debug("".join(map(str, [discid, last] + track_frames[:-1] + [ track_frames[-1] / 75 ])))
        return "".join(map(str, [discid, last] + track_frames[:-1] + [ track_frames[-1] / 75 ]))


    @need_last_fm_support
    def guess_from_name(self):
        clean_dirname = self.abs_dirname.strip(string.digits)
        #let's do a little search 
