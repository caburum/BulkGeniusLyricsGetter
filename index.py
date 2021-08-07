import requests
import json

import asyncio
from pyppeteer import launch
loop = asyncio.get_event_loop()
browser = None

from os import environ
from dotenv import load_dotenv
load_dotenv()
GENIUS_TOKEN = environ.get('GENIUS_TOKEN')

with open('songs.json') as file:
	songs = json.load(file)

# Fetch song lyrics
def fetchLyrics(url):
	async def handleReq(request):
		if request.resourceType in ['script', 'image', 'stylesheet', 'font', 'media']: # I blocked 'script' and it works but if it breaks try removing it
			await request.abort()
		else:
			await request.continue_()
	async def main():
		global browser
		if not browser:
			browser = await launch(
				headless=False
			)
		page = await browser.newPage()
		await page.setRequestInterception(True)
		page.on('request', lambda req: asyncio.ensure_future(handleReq(req)))
		await page.goto(url, timout=1000000)
		lyrics = await page.evaluate("Array.from(document.querySelectorAll('div[class*=\"Lyrics__Container\"]')).map(function (elem) { return elem.innerText }).join('\\n')")
		await page.close()
		# await browser.close()
		print(lyrics)
		return lyrics
	return loop.run_until_complete(main())

# Lookup Genuis song ID
def lookupSong(song, artist):
	search = requests.get(f"https://api.genius.com/search?q={song} - {artist}", headers={
		'Authorization': f'Bearer {GENIUS_TOKEN}',
	}).json()

	details = None
	for hit in search['response']['hits']:
		if hit['result']['primary_artist']['name'] == artist:
			details = hit['result']
			break

	if details:
		print(f"Found song \"{details['title']}\" by \"{details['primary_artist']['name']}\" - ID {details['id']}")
		fetchLyrics(details['url'])
	else:
		print(f"Could not find \"{song}\" by \"{artist}\"")

for song in songs[0:2]:
	lookupSong(song['title'], song['artist'])