from lyricsFetch import lyricsFetch
import sys

test = len(sys.argv) > 1 and sys.argv[1] == 'test'

ARTIST_COUNT = 5 if test else 10000
SONG_PER_ARTIST = 5 if test else 10000

for category in ['rock', 'rap', 'country', 'pop']:
	lf = lyricsFetch(category, ARTIST_COUNT, SONG_PER_ARTIST, verbose=False)
	lyric_file = open('data/'+category+'.txt', "w")
	while True:
		lset = lf.getNextLyricSet()
		if lset==None:
			break
		lyric_file.write(lset[2]+'\n\n<SONG_BOUNDARY>\n\n')
	lyric_file.close()