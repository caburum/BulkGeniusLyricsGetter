# BulkGeniusLyricsGetter

Scrape lyrics off of [Genius](https://genius.com) in bulk.

## Setup

You need to get a client access token from the [Genius API Clients manager](https://genius.com/api-clients). You will need to [create an account](https://genius.com/signup) or [new API client](https://genius.com/api-clients/new) if you don't already have them.

Add your token to `sample.env` and rename the file to `.env`.

## Adding songs

Add an array of your songs to `songs.json` (or copy `songs.sample.json`). Each song is an object with a `title` and `artist`, which will be looked up on Genius to find the correct lyrics.

Songs will be saved under `Artist - Song.txt` in the lyrics folder.
