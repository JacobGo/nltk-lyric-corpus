"""
Author: Nick Laurin
This handles fetching lyrics for the data generator
"""
import spotipy_api
from PyLyrics import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
import requests
import re
import lxml

class lyricsFetch():
	def __init__(self,genre,artistCount,tracksPerArtist,verbose=True):
		self.verbose = verbose
		self.genre = genre #('pop'),('country'),('rock'),('rap')
		#get Artists through spotipy
		client_credentials_manager = SpotifyClientCredentials()
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
		query = sp.search(q='genre:' + genre, type='artist', limit=artistCount)
		artistSet = [x['name'] for x in query['artists']['items']]
		songSet = defaultdict(list)
		if self.verbose:
			print "Artists are:"
			print artistSet
		for artist in artistSet:
			if self.verbose:
				print "~~~~~~~~~~~~~~~~~~~~"
				print artist
				print "~~~~~~~~~~~~~~~~~~~~"
			try:
				albums = PyLyrics.getAlbums(artist)
			except UnicodeEncodeError:
				if self.verbose:
					print "Artist has illegal character!"
				continue
			except ValueError:
				if self.verbose:
					print "Artist not in wikia lyrics!"
				continue
			for album in albums:
				if len(songSet[artist]) >= tracksPerArtist:
						break
				if self.verbose:
					print "------------"
					print album
					print "------------"
				songs = self.myGetTracks(album)
				for song in songs:
					if self.verbose:
						print song
					songSet[artist].append(song)
					if len(songSet[artist]) >= tracksPerArtist:
						break
		songList = []
		for artist, songs in songSet.items():
			songList.extend(songs)
		self.songIter = iter(songList)

	def myGetTracks(self,album):
		url = "http://lyrics.wikia.com/api.php?action=lyrics&artist={0}&fmt=xml".format(album.artist())
		#soup = BeautifulSoup(requests.get(url).text,"lxml")
		soup = BeautifulSoup(requests.get(url).text, "lxml-xml") 
		#soup = BeautifulSoup(requests.get(url).text, "xml")	

		for al in soup.find_all('album'):
			currentAlbum = al
			if al.text.lower().strip() == album.name.strip().lower():
				break
		songs = [Track(song.text,album,album.artist()) for song in currentAlbum.findNext('songs').findAll('item')]
		return songs
		

	def getNextLyricSet(self):
		"""Return the lyrics for a new existing song"""
		lyrics = None
		while lyrics is None:
			try:
				song = self.songIter.next() #throws StopIteration Exception. Needs to be caught anywhere this is used.
			except StopIteration:
				return None
			try:
				lyrics = PyLyrics.getLyrics(song.artist,song.name)
				if lyrics[:5] == '<span':
					lyrics = None
			except ValueError:
				if self.verbose:
					print "Song not in wikia lyrics!"
		artist = song.artist
		title = song.name
		return (title, artist, lyrics)

test = True
testFile = open("test.txt", "w")
if test:
	lf = lyricsFetch('country',2,2, verbose=False)
	#print lf.songSet
	for n in range(9):
		print lf.getNextLyricSet()