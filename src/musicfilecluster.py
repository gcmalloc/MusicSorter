try:
    import lastfm
    last_fm_support = True
except ImportError:
    last_fm_support = False
    
def need_last_fm_support(f):
    wrapper(args*, kwargs**):
        if last_fm_support:
            f()
        else:
            logging.error("no last fm support")
"""
Implementation of a MusicFileCluster. This is a representation of music
that belong to the same directory. This permit to take in consideration
their proximity in the directory tree
"""


class MusicFileCluster(object):

    """
    Constructor that take the absolute dirname and a number of musicFile.
    """
    def __init__(self, abs_dirname, musicFile*):
        self._musicFiles = set()
        for i in musicFile:
            self._musicFile.add(i)
        self._abs_dirname = dirname

    def add(self, musicFile):
        self._musicFiles.add(musicFile)

    def weight_files():
        #files are together so they should look a bit the same
        pass

def disc_idmp3(cd):
    last = len(cd)

    track_frames = []
    checksum = 0
    cdtime = 0
    
    adjust = 0
#    f.getPlayTime()
#if eyeD3.isMp3File(f):
#     audioFile = eyeD3.Mp3AudioFile(f)
#     tag = audioFile.getTag()

    print
    for i in range(0, last):
    #   mf = mad.MadFile(cd[i-1])    #madfile length calculation not that good
    #   ms = mf.total_time()
        try:
            audioFile = eyeD3.Mp3AudioFile(cd[i-1]) #read the music file
        except eyeD3.tag.TagException, value:
            print avkutil.color(value,'lred')
        br = audioFile.getBitRate() #bitrate
        pt = audioFile.getPlayTimeString()#number o  time the music is playeds
        ms = audioFile.playTime * 1000 #playtime in milisecond
        ms = ms + adjust #add ajust time for the  rest
        if i == 0:
            ms = 2000
        cdtime = cdtime + ms
        (min, sec, frame) = (cdtime/60000,(cdtime%60000)/1000, (((cdtime%60000)%1000)*75)/1000 )
        print '%02d:%02d.%02d  vbr=%d br=%d %s %s' %(min,sec,frame,br[0],br[1],pt,cd[i-1])
        checksum = checksum + DiscID.cddb_sum(min*60 + sec)
        track_frames.append(min*60*75 + sec*75 + frame)

    audioFile = eyeD3.Mp3AudioFile(cd[-1])
    ms = audioFile.playTime * 1000
    ms = ms + adjust
    cdtime = cdtime + ms
    (min, sec, frame) = (cdtime/60000,(cdtime%60000)/1000, (((cdtime%60000)%1000)*75)/1000 )
    track_frames.append(min*60*75 + sec*75 + frame)

    total_time = (track_frames[-1] / 75) - (track_frames[0] / 75)
           
    discid = ((checksum % 0xff) << 24 | total_time << 8 | last)

    for i in range(0, last-1):
    secs = (track_frames[i+1] - track_frames[i])/75
    min = secs/60
    sec = secs%60
    print '%02d:%02d' %(min,sec)

    return [discid, last] + track_frames[:-1] + [ track_frames[-1] / 75 ]


    @last_fm_support
    def guess_from_name(self):
        clean_dirname = self.abs_dirname.strip(string.digits)
        #let's do a little search 
