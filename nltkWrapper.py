'''
Author: Jacob Goldman
NLTK CorpusReader for the song lyrics corpus
'''
from nltk.corpus.reader.api import *
from nltk.tokenize import *

class Song(object):

	def __init__(self, title=None, stanzas=None):
		self.title = title
		if stanzas is None:
			self.stanzas = []
		else:
			self.stanzas = lines

	def lines(self):
		lines = []
		for stanza in self.stanzas:
			for line in stanza.lines:
				lines.append(line)
			lines.append('\n')
		return lines

	def words(self):
		words = []
		for line in self.lines():
			words += WordPunctTokenizer().tokenize(line)
		return words

	def add_stanzas(self, stanza):
		self.stanzas.append(stanza)

	def __repr__(self):
		return 'Song(title="{}", stanzas={})'.format(self.title, self.stanzas)

class Stanza(object):

	def __init__(self, lines):
		self.lines = lines
		# here is where rhyme annotations would go

	def __repr__(self):
		return('Stanza(lines={})').format(self.lines)

class SongCorpusReader(CorpusReader):
	CorpusView = StreamBackedCorpusView

	def __init__(self, root=None, fileids=None, word_tokenizer=WordPunctTokenizer(), encoding='utf8'):
		if root is None:
			root = './data'
		if fileids is None:
			fileids = os.listdir('./data')
		CorpusReader.__init__(self,root,fileids,encoding)
		self._word_tokenizer = word_tokenizer

	def raw(self, fileids=None):
		if fileids is None: fileids = self._fileids
		elif isinstance(fileids, string_types): fileids = [fileids]
		raw_texts = []
		for f in fileids:
			_fin = self.open(f)
			raw_texts.append(_fin.read())
			_fin.close()
		return concat(raw_texts)

	def words(self, fileids=None):
		return concat([self.CorpusView(path, self._read_word_block, encoding=enc)
						for (path, enc, fileid)
						in self.abspaths(fileids, True, True)])
	def songs(self, fileids=None):
		return concat([self.CorpusView(path, self._read_song_block, encoding=enc)
						for (path, enc, fileid)
						in self.abspaths(fileids, True, True)])

	def _read_song_block(self,stream):
		songs = []
		song = Song()
		while True:
			song.add_stanzas(self._read_stanza_block(stream))
			oldpos = stream.tell()
			line = stream.readline()
			if line=='<SONG_BOUNDARY>\n':
				songs.append(song)
				song = Song()
			else:
				stream.seek(oldpos)

			if not line:
				return songs

	def _read_stanza_block(self,stream):
		lines = []
		while True:
			line = stream.readline()
			if line != '\n': 
				if line: line = line[:len(line)-1]
				lines.append(line)
			if line == '\n' or not line:
				return Stanza(lines)

	def _read_word_block(self, stream):
		words = []
		for i in range(20):
			line = stream.readline()
			if line != '<SONG_BOUNDARY>' and line != '<SONG_BOUNDARY>\n':
				words.extend(self._word_tokenizer.tokenize(line))
		return words

